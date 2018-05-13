import sqlite3
import os
import pickle
from pprint import PrettyPrinter
from constants import (TEAM_NAMES, DB_PATH, RUSH_TYPES, ROUTE_TYPES)
from utils import avg_cols

PICKLE_DIR = "../efficacies/pickles"  # directory to store pickled dictionaries
REPICKLE = False                      # override existing pickles

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()
pp = PrettyPrinter(width=100)

# build rush defense averages (average yards yielded per attempt, by type)
print("Analyzing rush defenses...")
rush_def_avgs_fname = "%s/rush_def_avgs.pkl" % PICKLE_DIR
if os.path.exists(rush_def_avgs_fname) and not REPICKLE:
    print("Already exists, skipping.")
    with open(rush_def_avgs_fname, "rb") as file:
        rush_def_avgs = pickle.load(file)
else:
    col_out_tmpl = "AVG(%s__per_att) %s__avg_per_att"
    col_in_tmpl = "SUM(%s__yds) / SUM(%s__att) %s__per_att"
    col_out = ",".join([col_out_tmpl % (typ, typ) for typ in RUSH_TYPES])
    col_in = ",".join([col_in_tmpl % (typ, typ, typ) for typ in RUSH_TYPES])
    rush_def_avgs = {"league_avg": []}
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
        res = list(c.fetchone())
        rush_def_avgs[team] = res
        rush_def_avgs["league_avg"].append(res)
    rush_def_avgs["league_avg"] = avg_cols(rush_def_avgs["league_avg"])
    with open(rush_def_avgs_fname, "wb") as file:
        pickle.dump(rush_def_avgs, file)

print("Analyzing pass defenses...")
pass_def_avgs_fname = "%s/pass_def_avgs.pkl" % PICKLE_DIR
if os.path.exists(pass_def_avgs_fname) and not REPICKLE:
    print("Already exists, skipping.")
    with open(pass_def_avgs_fname, "rb") as file:
        pass_def_avgs = pickle.load(file)
else:
    col_out_tmpl1 = "AVG(%s__ctch_per_tgt) %s__avg_ctch_per_tgt"
    col_in_tmpl1 = "SUM(%s__ctch) / SUM(%s__tgt) %s__ctch_per_tgt"
    col_out_tmpl2 = "AVG(%s__yds_per_ctch) %s__avg_yds_per_ctch"
    col_in_tmpl2 = "SUM(%s__yds) / SUM(%s__ctch) %s__yds_per_ctch"
    col_out_arr = []
    col_in_arr = []
    for typ in ROUTE_TYPES:
        col_out_arr.append(col_out_tmpl1 % (typ, typ))
        col_out_arr.append(col_out_tmpl2 % (typ, typ))
        col_in_arr.append(col_in_tmpl1 % (typ, typ, typ))
        col_in_arr.append(col_in_tmpl2 % (typ, typ, typ))
    col_out = ",".join(col_out_arr)
    col_in = ",".join(col_in_arr)
    pass_def_avgs = {"league_avg": []}
    for team in TEAM_NAMES:
        c.execute("""
            SELECT %s
                FROM (
                    SELECT %s
                    FROM tgt_dir td
                        JOIN snap_count sc ON
                            td.player_link = sc.player_link AND
                            td.game = sc.game
                    GROUP BY td.game, sc.team_name
                    HAVING td.game LIKE ? AND
                           sc.team_name NOT LIKE ?
                )
        """ % (col_out, col_in), ["%%%s%%" % team.replace(" ", "_"), team])
        res = list(c.fetchone())
        pass_def_avgs[team] = res
        pass_def_avgs["league_avg"].append(res)
    pass_def_avgs["league_avg"] = avg_cols(pass_def_avgs["league_avg"])
    with open(pass_def_avgs_fname, "wb") as file:
        pickle.dump(pass_def_avgs, file)

print("Done.")
