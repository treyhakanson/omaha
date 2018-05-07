import os
import re
from pprint import PrettyPrinter
import csv
from bs4 import BeautifulSoup as bs
from utils import soupify_comment

# directory containing raw, unprocessed HTML documents
FILE_DIR = "../raw/boxscores"

# Route information
ROUTE_TYPES = ["short_l", "short_mid", "short_r", "deep_l", "deep_mid",
               "deep_r"]
ROUTE_ATTRS = ["tgt", "ctch", "yds", "td"]

# Rush information
RUSH_TYPES = ["l_end", "l_tckl", "l_guard", "mid", "r_guard", "r_tckl",
              "r_end"]
RUSH_ATTRS = ["att", "yds", "td"]

# Defensive information
PASS_TCKL_TYPES = ["short_r", "short_mid", "short_l", "deep_r", "deep_mid",
                   "deep_l"]
TCKL_ATTRS = ["tckl", "dfnd"]

# Snap count information
SNAP_COUNT_TYPES = ["off", "def", "st"]
SNAP_COUNT_ATTRS = ["num", "pct"]
SNAP_COUNT_PRE_COLS = ["pos"]

# Final output directory information
ROOT_DIR = "../boxscore-data"
OUTPUT_DIRS = [
    "tgt_dirs",
    "rush_dirs",
    "pass_tckls",
    "rush_tckls",
    "snap_counts",
    "zebras",
    "penalties"
]

# Pipline information; set to false to ignore
PIPELINE = {
    "TGT_DIRS": True,
    "RUSH_DIRS": True,
    "PASS_TCKLS": True,
    "RUSH_TCKLS": True,
    "SNAP_COUNTS": True,
    "ZEBRAS": True,
    "PENALTIES": True,
}
# if true, will only attempt to process 1 boxscore
DEV_MODE = False
# if false, will not attempt to output csv data
OUTPUT = True
# if the file has already been parsed, skip it
SKIP_EXISTING = True  # TODO: actually implement this


pp = PrettyPrinter(compact=True)
output_map = {}


def getweek(s):
    '''get the week number out of a filename.'''
    return re.match(r"\d{4}\.week(\d{1,2})\..*\.htm", s).group(1)


def getyear(s):
    '''get the year number out of a filename.'''
    return re.match(r"(\d{4})\.week\d{1,2}\..*\.htm", s).group(1)


def parse_table(soup, table_id, types=[], attrs=[], pre_cols=[], cast=True,
                drop_leading=1):
    soup = soupify_comment(soup, "all_%s" % table_id)
    header = ["player_name", "player_link"]
    for col in pre_cols:
        header.append(col)
    if len(types) > 0:
        for type in types:
            for attr in attrs:
                col = "%s__%s" % (type, attr)
                header.append(col)
    else:
        for attr in attrs:
            header.append(attr)
    res = [header]
    trs = soup.find("table", {"id": table_id}).tbody.find_all("tr")
    for tr in trs:
        # skip the interior header (separates teams)
        if "thead" in tr.get("class", []):
            continue
        player_name = tr.th.get_text()
        # functions as a unique identifier
        player_link = tr.th.a["href"]
        tds = tr.find_all("td")[drop_leading:]
        # using this instead of len(tds) because some box scores have some
        # random extra columns
        incr = (len(types) or 1) * (len(attrs) or 1) + len(pre_cols)
        player_res = []
        for i in range(incr):
            player_res.append(tds[i].get_text() or "0")
        if cast:
            player_res = list(map(lambda x: int(x), player_res))
        player_res = [player_name, player_link, *player_res]
        res.append(player_res)
    return res


def parse_zebras(soup, game):
    soup = soupify_comment(soup, "all_officials")
    res = [["zebra_name", "zebra_link", "role", "game"]]
    for tr in soup.find("table", {"id": "officials"}).find_all("tr")[1:]:
        role = tr.th.get_text()
        zebra_name = tr.td.get_text()
        zebra_link = tr.td.a["href"]
        res.append([zebra_name, zebra_link, role, game])
    return res


def parse_penalties(soup):
    soup = soupify_comment(soup, "all_pbp")
    res = [["player_name", "pen", "yds"]]
    re_str = (r".*Penalty on "  # prefix
              r"([^:]+): "      # player/team name
              r"([A-Za-z\s]+)"  # penalty type
              r"(, (\d+))?")    # yards (if accepted)
    prog = re.compile(re_str)
    for tr in soup.tbody.find_all("tr"):
        if "thead" in tr.get("class", []):
            continue
        play = tr.find_all("td")[4].get_text()
        if "Penalty" in play:
            m = prog.match(play)
            player_name = m.group(1)
            pen = m.group(2)
            yds = int(m.group(4)) if m.group(4) else -1  # -1 means declined
            res.append([player_name, pen, yds])
    return res


def parse_snap_counts(soup, home_team, away_team):
    home_sc = parse_table(soup, "home_snap_counts", types=SNAP_COUNT_TYPES,
                          attrs=SNAP_COUNT_ATTRS,
                          pre_cols=SNAP_COUNT_PRE_COLS,
                          cast=False,
                          drop_leading=0)
    away_sc = parse_table(soup, "vis_snap_counts", types=SNAP_COUNT_TYPES,
                          attrs=SNAP_COUNT_ATTRS,
                          pre_cols=SNAP_COUNT_PRE_COLS,
                          cast=False,
                          drop_leading=0)[1:]
    header = [*home_sc[0], "team_name"]
    home_sc = home_sc[1:]
    for row in home_sc:
        row[3:] = list(map(lambda x: int(x.strip("%")), row[3:]))
        row.append(home_team)
    for row in away_sc:
        row[3:] = list(map(lambda x: int(x.strip("%")), row[3:]))
        row.append(away_team)
    return [header, *home_sc, *away_sc]


fnames = os.listdir(FILE_DIR)
fnames.sort(key=getweek)

for fname in fnames:
    html = open("%s/%s" % (FILE_DIR, fname), "r")
    soup = bs(html, "html.parser")
    game = soup.h1.get_text().split(" - ")[0]
    week = getweek(fname)
    year = getyear(fname)
    print("Processing %s week %s, %s..." % (year, week, game))
    if PIPELINE["TGT_DIRS"]:
        output_map["tgt_dirs"] = parse_table(soup, "targets_directions",
                                             types=ROUTE_TYPES,
                                             attrs=ROUTE_ATTRS)
    if PIPELINE["RUSH_DIRS"]:
        output_map["rush_dirs"] = parse_table(soup, "rush_directions",
                                              types=RUSH_TYPES,
                                              attrs=RUSH_ATTRS)
    if PIPELINE["PASS_TCKLS"]:
        output_map["pass_tckls"] = parse_table(soup, "pass_tackles",
                                               types=PASS_TCKL_TYPES,
                                               attrs=TCKL_ATTRS)
    if PIPELINE["RUSH_TCKLS"]:
        output_map["rush_tckls"] = parse_table(soup, "rush_tackles",
                                               attrs=RUSH_TYPES)
    if PIPELINE["SNAP_COUNTS"]:
        away_team, home_team = game.split(" at ")
        output_map["snap_counts"] = parse_snap_counts(soup, home_team,
                                                      away_team)
    if PIPELINE["ZEBRAS"]:
        output_map["zebras"] = parse_zebras(soup, game)
    if PIPELINE["PENALTIES"]:
        output_map["penalties"] = parse_penalties(soup)
    res_base_fname = game.replace(" at ", "@").replace(" ", "_")
    res_fname = "%s.week%s.%s.csv" % (year, week, res_base_fname)
    for output_dir in OUTPUT_DIRS:
        if not OUTPUT:
            break
        if not PIPELINE[output_dir.upper()]:
            continue
        with open("%s/%s/%s" % (ROOT_DIR, output_dir, res_fname), "w") as file:
            writer = csv.writer(file)
            for row in output_map[output_dir]:
                writer.writerow(row)
    if DEV_MODE:
        break
