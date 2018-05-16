import pickle
from pprint import PrettyPrinter
import argparse
from matplotlib import pyplot as plt
import numpy as np
import mplcursors
from constants import (EFF_PKL_DIR, TEAM_NAMES, TEAM_COLORS, RUSH_TYPES,
                       ROUTE_TYPES)


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
    sel.annotation.set_text(sel.artist.get_label())
    sel.annotation.get_bbox_patch().set(fc="white")


def plot_wks(rdap, wk_str, ctgy, teams, types, is_rush=True, lobf=False):
    idx = types.index(ctgy)
    if "-" in wk_str:
        start, stop = list(map(lambda x: int(x), wk_str.split("-")))
        wks = range(start - 1, stop)
    else:
        wks = [int(wk_str) - 1]
    for team in teams:
        team_x = []
        team_y = []
        c = TEAM_COLORS[team].primary
        ec = TEAM_COLORS[team].secondary
        for wk in wks:
            if rdap[team][wk] is None:
                continue  # skip bye week
            wk_data = list(rdap[team][wk])
            group_sz = 2 if is_rush else 3
            subs = subgroup(wk_data, group_sz)[idx]
            if is_rush:
                y, x = subs
            else:
                y, _, x = subs
            s = "Att" if is_rush else "Tgt"
            label = "(Week %d)\n%s\n%s: %d\nYds: %d" % (wk + 1, team, s, x, y)
            plt.scatter(x, y, c=c, edgecolors=ec, linewidth=1, label=label)
            team_x.append(x)
            team_y.append(y)
        x = np.unique(team_x)
        poly = np.poly1d(np.polyfit(team_x, team_y, 1))
        if lobf:
            plt.plot(x, poly(x), c=c, label=team)
    s = "Attempt" if is_rush else "Target"
    plt.xlabel(s)
    plt.ylabel("Yards")
    team_str = ", ".join(teams) if len(teams) <= 3 else "Team"
    plt.title("Yards per %s %s by %s (Week %s)"
              % (ctgy.upper(), s, team_str, wk_str))
    mplcursors.cursor(hover=True).connect("add", configure_popup)
    plt.show()


def plot_avgs(dap, ctgy, teams, types, is_rush=True, lobf=False):
    idx = types.index(ctgy)
    for team in teams:
        team_x = []
        team_y = []
        c = TEAM_COLORS[team].primary
        ec = TEAM_COLORS[team].secondary
        for wk in range(17):
            if dap[team][wk] is None:
                continue  # skip bye week
            wk_data = list(dap[team][wk])
            group_sz = 2 if is_rush else 3
            subs = subgroup(wk_data, group_sz)[idx]
            if is_rush:
                y, x = subs
            else:
                y, _, x = subs
            if x <= 0:
                continue  # ignore weeks with no attempts
            ypa = y / x
            s = "att" if is_rush else "tgt"
            label = "%s\n%.2f yds/%s" % (team, ypa, s)
            plt.scatter(wk, ypa, c=c, edgecolors=ec, linewidth=1, label=label)
            team_x.append(wk)
            team_y.append(ypa)
        x = np.unique(team_x)
        poly = np.poly1d(np.polyfit(team_x, team_y, 1))
        if lobf:
            plt.plot(x, poly(x), c=c, label=team)
    s = "Attempt" if is_rush else "Target"
    plt.xlabel("Week")
    plt.ylabel("Yards per %s" % s)
    team_str = ", ".join(teams) if len(teams) <= 3 else "Team"
    plt.title("Yards per %s per Week by %s" % (s, team_str))
    mplcursors.cursor(hover=True).connect("add", configure_popup)
    plt.show()


pp = PrettyPrinter(width=100)

parser = argparse.ArgumentParser(description="Visualize defensive efficacies")
parser.add_argument("ctgy", metavar="ctgy", type=str, nargs=1,
                    help="The category to analyze")
parser.add_argument("teams", metavar="teams", type=str, nargs="*",
                    default=TEAM_NAMES,
                    help="The specific teams to analyze")
parser.add_argument("--weeks", dest="wks", type=str, nargs=1,
                    help=("The range of weeks to analyze. If no value is "
                          "provided, will apply an average instead."))
parser.add_argument("--showlines", dest="lobf", action="store_true",
                    help="Show lines of best fit for data sets")
args = parser.parse_args()

if args.ctgy[0] in RUSH_TYPES:
    is_rush = True
    typ = "rush"
    types = RUSH_TYPES
else:
    is_rush = False
    typ = "pass"
    types = ROUTE_TYPES

file = open("%s/%s_def_avgs_partial.pkl" % (EFF_PKL_DIR, typ), "rb")
dap = pickle.load(file)
file.close()

if args.wks is not None:
    plot_wks(dap, args.wks[0], args.ctgy[0], args.teams, types,
             is_rush=is_rush, lobf=args.lobf)
else:
    plot_avgs(dap, args.ctgy[0], args.teams, types, is_rush=is_rush,
              lobf=args.lobf)
