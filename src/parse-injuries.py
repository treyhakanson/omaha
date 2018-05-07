import os
from bs4 import BeautifulSoup as bs
from utils import getweek
import csv

COLUMN_NAMES = ["Player", "Injury", "Wed", "Thu", "Fri", "Status"]
RAW_FILE_DIR = "../raw/injuries"
RES_FILE_DIR = "../injuries"

fnames = os.listdir(RAW_FILE_DIR)
fnames.sort(key=getweek)

for fname in fnames:
    print("Parsing %s..." % fname)
    # ps = practice status
    res = [["player_name", "team", "injury", "wed_ps", "thu_ps", "fri_ps",
            "final"]]
    html = open("%s/%s" % (RAW_FILE_DIR, fname), "r")
    soup = bs(html, "html.parser")
    html.close()
    tables = soup.find_all("table", {"class": "statistics"})
    for table in tables:
        team_name = table.previous_sibling.get_text()
        cells = table.tbody.find_all("td")
        i = 0
        while i < len(cells):
            player = cells[i].find("span", {"class": "hidden-xs"}).get_text()
            injury = cells[i + 1].get_text()
            practices = list(map(lambda x: x.get_text(),
                                 cells[(i + 2):(i + 5)]))
            try:
                status = cells[i + 5].b.get_text()
            except Exception as e:
                status = "Available"
            res.append([player, team_name, injury, *practices, status])
            i += 6
    with open("%s/%s.csv" % (RES_FILE_DIR, fname[:-5]), "w") as file:
        writer = csv.writer(file)
        for row in res:
            writer.writerow(row)
print("Done.")
