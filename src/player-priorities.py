import sqlite3
from functools import reduce
from pprint import PrettyPrinter
import csv
from utils import build_header
from constants import (DB_PATH, PASS_TCKL_TYPES, RUSH_TYPES, TCKL_ATTRS,
                       DEF_POS)

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

# Pipeline information
PIPELINE = {
    "PASS_DEF": True,
    "RUSH_DEF": True,
    "RUSH_OFF": True,
    "PASS_OFF": True,
    "REC_OFF": True
}

pp = PrettyPrinter(width=100)
conn = sqlite3.connect(DB_PATH)
c = conn.cursor()


def weight_priorities(data, i, j):
    res = [*data[i:j]]
    sum = reduce(lambda x, y: x + y, res)
    res = list(map(lambda x: x / sum, res))
    return res


def defensive_priorities(table_name, types=[], attrs=[], pos=[], fname=[]):
    header = build_header(types=types, attrs=attrs)
    header_str = ", ".join(map(lambda x: "SUM(%s) %s" % (x, x), header))
    sub_str = ",".join("?" * len(pos))
    c.execute("""
        SELECT t.player_name,
               sc.pos,
               sc.team_name,
               SUM(def__num) def__num,
               %s -- dynamically created column names based on types/attrs
            FROM %s t
                JOIN snap_count sc ON
                    t.player_link = sc.player_link AND
                    t.game = sc.game
            WHERE sc.pos IN (%s)
            GROUP BY t.player_link
            HAVING def__num > ?
        ORDER BY sc.team_name, sc.pos
    """ % (header_str, table_name, sub_str), [*pos, SNAP_THRESH__DEF])
    res = c.fetchall()
    with open(fname, "w") as file:
        writer = csv.writer(file)
        for player in res:
            player = list(player)
            player[5:] = weight_priorities(player, 4, len(res))
            writer.writerow(player)


if PIPELINE["PASS_DEF"]:
    print("Processing pass defense priorities...")
    fname = "%s/pass_defense.csv" % FILE_DIR
    defensive_priorities("pass_tckl", types=PASS_TCKL_TYPES, attrs=TCKL_ATTRS,
                         pos=DEF_POS, fname=fname)

if PIPELINE["RUSH_DEF"]:
    print("Processing rush defense priorities...")
    fname = "%s/rush_defense.csv" % FILE_DIR
    defensive_priorities("rush_tckl", attrs=RUSH_TYPES, pos=DEF_POS,
                         fname=fname)

print("Done.")
