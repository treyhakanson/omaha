import sqlite3
from functools import reduce
from pprint import PrettyPrinter
import csv
from utils import build_header, log_query
from constants import (DB_PATH, PASS_TCKL_TYPES, RUSH_TYPES, TCKL_ATTRS,
                       DEF_POS, SEC_POS, BACK_POS, REC_POS, ALL_POS,
                       ROUTE_TYPES)

"""
Determining secondary player productivity is difficult since tackles are not a
particularly strong indicator of success. If anything, tackles by secondary
players on non-running plays suggest someone in the secondary allowed a catch,
so they are almost a negative indicator (excluding plays like screens, or
catches by players covered by linebackers, with should be to tight ends
primarily).

My initial thoughts on how to cope, and implications in general:

- Passes defended should be weighted highly, as those are objectively
  "good plays" for a defender.
- Tackles should be weighted lowly, if not negatively, for certain secondary
  positions and situations
- It may be useful to incorporate a ratio of quantity of actions performed to
  snap count for certain secondary players. For example, if a cornerback is on
  the field for a high volumne of snaps and performs no actions, than the
  players they were covering we likely no targeted. Either that, or they
  consitently gave up touchdowns. This information should be verifiable based
  on receiver performance
- Based on the above, the ideal defense would have corners with a small action
  quantity to snap count ratio, and linebackers/linemen with the bulk of the
  tackles (may or may not be true).

Things to keep in mind/concerns:

- If a receiver makes a catch/back rushed and runs out of bounds, how is this
  recorded? Can check to see if its recorded as a tackle by seeing if
  `(run_tckls + pass_tckls) - (rushes + receptions) + TDs` is negative
"""

FILE_DIR = "../priorities"  # output directory

TCKL_WEIGHT = 1.0  # Weight of tackles made
DFND_WEIGHT = 2.0  # Weight of passes defended
QUAN_WEIGHT = 1.1  # Weight of quantity of actions

# Minimum number of snaps for a player to be considered (defense)
SNAP_THRESH__DEF = 16
SNAP_THRESH__OFF = 16

# Pipeline information
PIPELINE = {
    "PASS_DEF": True,
    "RUSH_DEF": True,
    "RUSH_OFF": True,
    "PASS_OFF": True,
    "REC_OFF": True
}


def weight_priorities(data, i, j):
    res = [*data[i:j]]
    sum = reduce(lambda x, y: x + y, res)
    res = list(map(lambda x: x / sum, res))
    return res


def build_priorities(cursor, table_name, cols, pos=ALL_POS,
                     fname="./priorities.csv", defense=True, log_only=False):
    """
    Generates a CSV containing player priorities based on the given values. The
    Table given will be joined with the snap_count table, and thus the given
    table must have `game` and `player_link` columns. Resultant data will be
    prefixed with the following columns: `player_name`, `pos`, `team_name`, and
    `snap_count` (total number of snaps taken on the year)

    Params:
    cursor (cursor) - the database cursor to execute the query on.
    table_name (str) - the name of the table to build priorities for
    header (arrayOf(str)) - the columns to consider for building priorities
    pos (arrayOf(str)) - the positions to consider from the table
    fname (str) - the name of the file to output to
    defense (bool) - whether or not the prioritization is for defensive players
    log_only (bool) - if true, will simply output the query rather than execute
    """
    header_str = ",".join(map(lambda x: "SUM(%s) %s" % (x, x), cols))
    sub = ",".join("?" * len(pos))
    side = "def__num" if defense else "off__num"
    THRESH = SNAP_THRESH__DEF if defense else SNAP_THRESH__OFF
    query = """
        SELECT t.player_name,
               sc.pos,
               sc.team_name,
               SUM(%s) snap_num,
               %s -- dynamically created column names based on types/attrs
            FROM %s t
                JOIN snap_count sc ON
                    t.player_link = sc.player_link AND
                    t.game = sc.game
            WHERE sc.pos IN (%s)
            GROUP BY t.player_link
            HAVING %s > ? -- TODO: change this from minimum snap count to
                          -- minimum attempts (for offense)
        ORDER BY sc.team_name, sc.pos
    """ % (side, header_str, table_name, sub, side)
    query_args = [*pos, THRESH]
    if log_only:
        log_query(cursor, query, query_args)
        return
    cursor.execute(query, query_args)
    res = cursor.fetchall()
    with open(fname, "w") as file:
        writer = csv.writer(file)
        writer.writerow(["player_name", "pos", "team_name", "snap_num", *cols])
        for player in res:
            player = list(player)
            player[4:] = weight_priorities(player, 4, len(res))
            writer.writerow(player)


pp = PrettyPrinter(width=100)
conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

if PIPELINE["PASS_DEF"]:
    print("Processing pass defense priorities...")
    fname = "%s/pass_def.csv" % FILE_DIR
    cols = build_header(types=PASS_TCKL_TYPES, attrs=TCKL_ATTRS)
    build_priorities(c, "pass_tckl", cols, pos=SEC_POS, fname=fname)

if PIPELINE["RUSH_DEF"]:
    print("Processing rush defense priorities...")
    fname = "%s/rush_def.csv" % FILE_DIR
    cols = build_header(attrs=RUSH_TYPES)
    build_priorities(c, "rush_tckl", cols, pos=DEF_POS, fname=fname)

if PIPELINE["RUSH_OFF"]:
    print("Processing rushing offense priorities...")
    fname = "%s/rush_off.csv" % FILE_DIR
    cols = build_header(types=RUSH_TYPES, attrs=["att"])
    pos = [*BACK_POS, "WR"]
    build_priorities(c, "rush_dir", cols, pos=pos, fname=fname, defense=False)

if PIPELINE["REC_OFF"]:
    print("Processing receiving offense priorities...")
    fname = "%s/rec_off.csv" % FILE_DIR
    cols = build_header(types=ROUTE_TYPES, attrs=["tgt"])
    pos = [*BACK_POS, *REC_POS]
    build_priorities(c, "tgt_dir", cols, pos=pos, fname=fname, defense=False)

if PIPELINE["PASS_OFF"]:
    print("Processing passing offense priorities...")
    # TODO: complete body

print("Done.")
