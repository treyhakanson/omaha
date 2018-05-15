import sqlite3
import os
import pickle
from pprint import PrettyPrinter
from constants import (TEAM_NAMES, DB_PATH, RUSH_TYPES, ROUTE_TYPES,
                       EFF_PKL_DIR)
from utils import avg_cols

REPICKLE = True  # override existing pickles

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()
pp = PrettyPrinter(width=100)


# NOTE: this weights all per game averages equally. This is likely not desired,
# since something like 1 carry for -3 yards one game would skew a 20 carry, 100
# yd game by an unproportional amount

def execute_full_def_query(cursor, table_name, col_out, col_in):
    """
    Executes a full query for each team; this provides season averages, as well
    as league averages
    """
    def_avgs = {"league_avg": []}
    for team in TEAM_NAMES:
        query_args = ["%%%s%%" % team.replace(" ", "_"), team]
        c.execute("""
            SELECT %s
                FROM (
                    SELECT %s
                    FROM %s t
                        JOIN snap_count sc ON
                            t.player_link = sc.player_link AND
                            t.game = sc.game
                    GROUP BY t.game, sc.team_name
                    HAVING t.game LIKE ? AND
                           sc.team_name NOT LIKE ?
                )
        """ % (col_out, col_in, table_name), query_args)
        res = list(c.fetchone())
        def_avgs[team] = res
        def_avgs["league_avg"].append(res)
    def_avgs["league_avg"] = avg_cols(def_avgs["league_avg"])
    def_avgs["header"] = [desc[0] for desc in cursor.description]
    return def_avgs


def execute_partial_def_query(cursor, table_name, col):
    """
    Executes a partial query for each team; this provides per-game results,
    rather than season averages in each category.
    """
    def_avgs = {}
    for team in TEAM_NAMES:
        query_args = ["%%%s%%" % team.replace(" ", "_"), team]
        c.execute("""
            SELECT %s
            FROM %s t
                JOIN snap_count sc ON
                    t.player_link = sc.player_link AND
                    t.game = sc.game
            GROUP BY t.game, sc.team_name
            HAVING t.game LIKE ? AND
                   sc.team_name NOT LIKE ?
        """ % (col, table_name), query_args)
        res = list(c.fetchall())
        def_avgs[team] = res
    def_avgs["header"] = [desc[0] for desc in cursor.description]
    return def_avgs


# build rush defense averages (average yards yielded per attempt, by type)
print("Analyzing rush defenses...")
rush_def_avgs_full_fname = "%s/rush_def_avgs_full.pkl" % EFF_PKL_DIR
rush_def_avgs_part_fname = "%s/rush_def_avgs_partial.pkl" % EFF_PKL_DIR
if (os.path.exists(rush_def_avgs_full_fname) and
        os.path.exists(rush_def_avgs_part_fname)) and not REPICKLE:
    print("Already exists, skipping.")
else:
    col_out_tmpl = "AVG(%s__per_att) %s__avg_per_att"
    col_in_tmpl = "SUM(%s__yds) / SUM(%s__att) %s__per_att"
    col_tmpl = ("SUM(%s__yds) %s__yds,"
                "SUM(%s__att) %s__att")
    col_out = ",".join([col_out_tmpl % (typ, typ) for typ in RUSH_TYPES])
    col_in = ",".join([col_in_tmpl % (typ, typ, typ) for typ in RUSH_TYPES])
    col = ",".join([col_tmpl % (typ, typ, typ, typ) for typ in RUSH_TYPES])
    rush_def_avgs_full = execute_full_def_query(c, "rush_dir", col_out, col_in)
    rush_def_avgs_partial = execute_partial_def_query(c, "rush_dir", col)
    with open(rush_def_avgs_full_fname, "wb") as file:
        pickle.dump(rush_def_avgs_full, file)
    with open(rush_def_avgs_part_fname, "wb") as file:
        pickle.dump(rush_def_avgs_partial, file)

print("Analyzing pass defenses...")
pass_def_avgs_full_fname = "%s/pass_def_avgs_full.pkl" % EFF_PKL_DIR
pass_def_avgs_part_fname = "%s/pass_def_avgs_partial.pkl" % EFF_PKL_DIR
if (os.path.exists(pass_def_avgs_full_fname) and
        os.path.exists(pass_def_avgs_part_fname)) and not REPICKLE:
    print("Already exists, skipping.")
else:
    col_out_tmpl1 = "AVG(%s__ctch_per_tgt) %s__avg_ctch_per_tgt"
    col_in_tmpl1 = "SUM(%s__ctch) / SUM(%s__tgt) %s__ctch_per_tgt"
    col_out_tmpl2 = "AVG(%s__yds_per_ctch) %s__avg_yds_per_ctch"
    col_in_tmpl2 = "SUM(%s__yds) / SUM(%s__ctch) %s__yds_per_ctch"
    col_tmpl = ("SUM(%s__yds) %s__yds,"
                "SUM(%s__ctch) %s__ctch,"
                "SUM(%s__tgt) %s__tgt")
    col_out_arr = []
    col_in_arr = []
    col_arr = []
    for typ in ROUTE_TYPES:
        col_out_arr.append(col_out_tmpl1 % (typ, typ))
        col_out_arr.append(col_out_tmpl2 % (typ, typ))
        col_in_arr.append(col_in_tmpl1 % (typ, typ, typ))
        col_in_arr.append(col_in_tmpl2 % (typ, typ, typ))
        col_arr.append(col_tmpl % (typ, typ, typ, typ, typ, typ))
    col_out = ",".join(col_out_arr)
    col_in = ",".join(col_in_arr)
    col = ",".join(col_arr)
    pass_def_avgs_full = execute_full_def_query(c, "tgt_dir", col_out, col_in)
    pass_def_avgs_partial = execute_partial_def_query(c, "tgt_dir", col)
    with open(pass_def_avgs_full_fname, "wb") as file:
        pickle.dump(pass_def_avgs_full, file)
    with open(pass_def_avgs_part_fname, "wb") as file:
        pickle.dump(pass_def_avgs_partial, file)

print("Done.")
