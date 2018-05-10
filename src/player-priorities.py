import sqlite3
from pprint import PrettyPrinter
from utils import build_header
from constants import DB_PATH, PASS_TCKL_TYPES, TCKL_ATTRS

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

TCKL_WEIGHT = 1.0  # weight of tackles made
DFND_WEIGHT = 2.0  # weight of passes defended
QUAN_WEIGHT = 1.1  # weight of quantity of actions

pp = PrettyPrinter(width=100)
conn = sqlite3.connect(DB_PATH)
c = conn.cursor()
c.execute("""
    SELECT player_link
        FROM player
""")
player_links = list(map(lambda x: x[0], c.fetchall()))
header = build_header(PASS_TCKL_TYPES, TCKL_ATTRS)
header_str = ', '.join(list(map(lambda x: "SUM(%s) %s" % (x, x), header)))
c.execute("""
    SELECT pt.player_name, sc.pos, sc.team_name, pt.game, SUM(def__num), %s
        FROM pass_tckl pt
            JOIN snap_count sc ON
                pt.player_link = sc.player_link AND
                pt.game = sc.game
        GROUP BY pt.player_link
    ORDER BY sc.pos, sc.team_name
""" % header_str)
res = c.fetchall()
pp.pprint(res)
