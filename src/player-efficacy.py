import sqlite3
import os
import pickle
from pprint import PrettyPrinter
from constants import (TEAM_NAMES, DB_PATH, RUSH_TYPES)

PICKLE_DIR = "../efficacies/pickles"

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()
pp = PrettyPrinter(width=100)

# build rush defense averages (average yards yielded per attempt, by type)
rush_def_avgs_fname = "%s/rush_def_avgs.pkl" % PICKLE_DIR
if os.path.exists(rush_def_avgs_fname):
    with open(rush_def_avgs_fname, "rb") as file:
        rush_def_avgs = pickle.load(file)
else:
    col_out_tmpl = "AVG(%s__per_att) %s__avg_per_att"
    col_in_tmpl = "SUM(%s__yds) / SUM(%s__att) %s__per_att"
    col_out = ",".join([col_out_tmpl % (typ, typ) for typ in RUSH_TYPES])
    col_in = ",".join([col_in_tmpl % (typ, typ, typ) for typ in RUSH_TYPES])
    rush_def_avgs = {}
    for team in TEAM_NAMES:
        c.execute("""
            SELECT %s
                FROM (
                    SELECT %s
                    FROM rush_dir rd
                        JOIN snap_count sc ON
                            rd.player_link = sc.player_link AND
                            rd.game = sc.game
                    GROUP BY rd.game, sc.team_name
                    HAVING rd.game LIKE ? AND
                           sc.team_name NOT LIKE ?
                )
        """ % (col_out, col_in), ["%%%s%%" % team.replace(" ", "_"), team])
        res = c.fetchall()
        rush_def_avgs[team] = res
    with open(rush_def_avgs_fname, "wb") as file:
        pickle.dump(rush_def_avgs, file)

pp.pprint(rush_def_avgs)
