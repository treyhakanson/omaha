import os
import re
from bs4 import BeautifulSoup as bs, Comment


# directory containing raw, unprocessed HTML documents
FILE_DIR = "./raw/boxscores"
# table ids to grab; comment out to ignore unwanted sections
TABLE_IDS = [
    "all_player_offense",
    "all_player_defense",
    "all_returns",
    "all_kicking",
    "all_home_starters",
    "all_vis_starters",
    "all_home_snap_counts",
    "all_vis_snap_counts",
    "all_targets_directions",
    "all_rush_directions",
    "all_pass_tackles",
    "all_rush_tackles",
    "all_home_drives",
    "all_vis_drives",
    "all_pbp"
]


def getweek(s):
    '''get the week number out of a filename.'''
    return re.match(r"\d{4}\.week(\d{1,2})\..*\.htm", s).group(1)


def soupify_comment(s, id, el="div"):
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


fnames = os.listdir(FILE_DIR)
fnames.sort(key=getweek)

for fname in fnames:
    html = open("%s/%s" % (FILE_DIR, fname), "r")
    soup = bs(html, "html.parser")
    for id in TABLE_IDS:
        comment_soup = soupify_comment(soup, id)
        print(comment_soup.prettify())
    break
