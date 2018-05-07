import os
import csv
import re
from bs4 import BeautifulSoup as bs
from utils import soupify_comment

FILE_DIR = "../raw/players"
OUTPUT_FILE = "../boxscore-data/players/all-players.csv"


def process_col(td):
    val = td.get_text()
    if ("." in val):
        return float(val)
    return int(val)


file = open(OUTPUT_FILE, "w")
writer = csv.writer(file)
writer.writerow(["player_name", "player_link", "ht", "wt", "_40yd", "bench",
                 "broad_jump", "shuttle", "_3cone", "vertical"])
fnames = os.listdir(FILE_DIR)
fnames.sort()
n = len(fnames)

for i, fname in enumerate(fnames):
    os.system('clear')
    print("(%d/%d) %s..." % (i + 1, n, fname))
    html = open("%s/%s" % (FILE_DIR, fname), "r")
    soup = bs(html, "html.parser")
    player_name = soup.find("h1", {"itemprop": "name"}).get_text()
    m = re.match(r"players\.([A-Z])\.(.+)\.htm", fname)
    player_link = "/players/%s/%s.htm" % (m.group(1), m.group(2))
    try:
        soup = soupify_comment(soup, "all_combine")
        values = list(map(process_col, soup.find_all("td")[1:]))
    except Exception as e:
        values = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    writer.writerow([player_name, player_link, *values])

file.close()
print("Done.")
