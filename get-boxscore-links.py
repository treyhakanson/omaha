import os
import re
from bs4 import BeautifulSoup as bs


LINKS_FNAME = "./raw/misc/boxscore-links.csv"
FILE_DIR = "./raw/schedules"


def getyear(s):
    return int(re.match(r"(\d+)\.week\d+\.htm", s).group(1))


def getweek(s):
    return int(re.match(r"2017\.week(\d+)\.htm", s).group(1))


links = open(LINKS_FNAME, "w")
fnames = os.listdir(FILE_DIR)
fnames.sort(key=getweek)

for fname in fnames:
    print("Getting boxscore links for %s..." % fname)
    year = getyear(fname)
    week = getweek(fname)
    html = open("%s/%s" % (FILE_DIR, fname), "r")
    soup = bs(html, "html.parser")
    html.close()
    tdtags = soup.find_all("td", {"class": "gamelink"})
    hrefs = list(map(lambda x: x.a['href'], tdtags))
    for href in hrefs:
        links.write("%d,%d,%s\n" % (year, week, href))

print("Done.")
links.close()
