'''
Parses injury reports for each week, and pickles them. Upon unpickling, the
structure is as follows:

injury_report = {
    "Team Name": [
        ["Player Name", "Injury Type", "Wed Practice Status",
         "Thu Practice Status", "Fri Practice Status", "Final Status"],
        ...
    ],
    ...
}

Where "Team Name" matches the names in constants.TEAM_NAMES
'''
import os
from bs4 import BeautifulSoup as bs
from constants import TEAM_NAMES
from utils import getweek
import pickle

COLUMN_NAMES = ["Player", "Injury", "Wed", "Thu", "Fri", "Status"]
RAW_FILE_DIR = "./raw/injuries"
RES_FILE_DIR = "./injuries"

fnames = os.listdir(RAW_FILE_DIR)
fnames.sort(key=getweek)

for fname in fnames:
    print("Parsing %s..." % fname)
    injury_data = {}
    for team_name in TEAM_NAMES:
        injury_data[team_name] = [[*COLUMN_NAMES]]
    html = open("%s/%s" % (RAW_FILE_DIR, fname), "r")
    soup = bs(html, "html.parser")
    html.close()
    tables = soup.find_all("table", {"class": "statistics"})
    for table in tables:
        team_name = table.previous_sibling.get_text()
        print("\tParsing injuries for %s..." % team_name)
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
            injury_data[team_name].append([player, injury, *practices, status])
            i += 6
    with open("%s/%s.pkl" % (RES_FILE_DIR, fname[:-5]), "wb") as file:
        pickle.dump(injury_data, file)
    print("")
print("Done.")
