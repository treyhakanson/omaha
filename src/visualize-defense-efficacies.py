import pickle
import os
from pprint import PrettyPrinter
from matplotlib import pyplot as plt
import mplcursors
from constants import EFF_PKL_DIR, TEAM_NAMES, TEAM_COLORS

TYPES = ["l_end",
         "l_tckl",
         "l_guard",
         "mid",
         "r_guard",
         "r_tckl",
         "r_end",
         "all"]


def subgroup(arr, sz):
    """splits an array into sub arrays of size `sz`"""
    res = []
    while len(arr) > sz:
        pc = arr[:sz]
        res.append(pc)
        arr = arr[sz:]
    res.append(arr)
    return res


def configure_popup(sel):
    att, yds = sel.target
    txt = "%s\nAtt: %d\nYds: %d" % (sel.artist.get_label(), att, yds)
    sel.annotation.set_text(txt)
    sel.annotation.get_bbox_patch().set(fc="white")


pp = PrettyPrinter(width=100)

with open("%s/rush_def_avgs_partial.pkl" % EFF_PKL_DIR, "rb") as file:
    typ = os.sys.argv[1]
    wk_str = os.sys.argv[2]
    if len(os.sys.argv) >= 4:
        team_names = [os.sys.argv[3]]
    else:
        team_names = TEAM_NAMES
    idx = TYPES.index(typ)
    if "-" in wk_str:
        start, stop = list(map(lambda x: int(x), wk_str.split("-")))
        wks = range(start - 1, stop)
    else:
        wks = [int(wk_str) - 1]
    rdap = pickle.load(file)
    pts = []
    for team in team_names:
        for wk in wks:
            # skip bye week
            if rdap[team][wk] is None:
                continue
            wk_data = list(rdap[team][wk])
            y, x = subgroup(wk_data, 2)[idx]
            c = TEAM_COLORS[team].primary
            ec = TEAM_COLORS[team].secondary
            p = plt.scatter(x, y, c=c, edgecolors=ec, linewidth=1, label=team)
            pts.append(p)
    plt.xlabel("Attempts")
    plt.ylabel("Yards")
    plt.title("Yards per %s Attempt by Team (Week %s)" % (typ, wk_str))
    mplcursors.cursor(hover=True).connect("add", configure_popup)
    plt.show()
