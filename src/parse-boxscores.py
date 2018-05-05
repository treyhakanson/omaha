import os
import re
from bs4 import BeautifulSoup as bs, Comment
from pprint import PrettyPrinter
import csv

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

# Final output directory information
ROOT_DIR = "../boxscore-data"
OUTPUT_DIRS = [
    "tgt_dirs",
    "rush_dirs",
    "pass_tckls",
    "rush_tckls",
    "zebras",
    "penalties"
]

# Pipline information; set to false to ignore
PIPELINE = {
    "TGT_DIRS": False,
    "RUSH_DIRS": False,
    "PASS_TCKLS": False,
    "RUSH_TCKLS": True,
    "ZEBRAS": False,
    "PENALTIES": False
}

pp = PrettyPrinter(compact=True)
output_map = {}


def getweek(s):
    '''get the week number out of a filename.'''
    return re.match(r"\d{4}\.week(\d{1,2})\..*\.htm", s).group(1)


def getyear(s):
    '''get the year number out of a filename.'''
    return re.match(r"(\d{4})\.week\d{1,2}\..*\.htm", s).group(1)


def soupify_comment(soup, id, el="div"):
    '''
    Retrieve comment from soup by id, and convert into a soup object.
    args:
        s (bs) - soup object to search
        id (str) - str id to find in s
    returns:
        retrieved comment as a soup object
    '''
    wrapper = soup.find(el, {"id": id})
    comment = wrapper.find(text=lambda txt: isinstance(txt, Comment))
    return bs(comment, "html.parser")


def parse_table(soup, table_id, types=[], attrs=[]):
    soup = soupify_comment(soup, "all_%s" % table_id)
    header = ["player_name", "player_link"]
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
        player_link = tr.th.a["href"]  # functions as a unique identifier
        tds = tr.find_all("td")[1:]  # drop team name
        i = 0
        incr = len(attrs)
        player_res = []
        while (i < len(tds)):
            for j in range(incr):
                player_res.append(tds[i + j].get_text() or "0")
            i += incr
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
    if PIPELINE["ZEBRAS"]:
        output_map["zebras"] = parse_zebras(soup, game)
    if PIPELINE["PENALTIES"]:
        output_map["penalties"] = parse_penalties(soup)
    res_base_fname = game.replace(" at ", "@").replace(" ", "_")
    res_fname = "%s.week%s.%s.csv" % (year, week, res_base_fname)
    for output_dir in OUTPUT_DIRS:
        if not PIPELINE[output_dir.upper()]:
            continue
        with open("%s/%s/%s" % (ROOT_DIR, output_dir, res_fname), "w") as file:
            writer = csv.writer(file)
            for row in output_map[output_dir]:
                writer.writerow(row)
