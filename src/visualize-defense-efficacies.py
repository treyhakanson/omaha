import pickle
from pprint import PrettyPrinter
from matplotlib import pyplot as plt
import mplcursors
from constants import EFF_PKL_DIR, TEAM_NAMES, TEAM_COLORS, RUSH_TYPES
import argparse


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


def configure_popup_avg(sel):
    wk, ypa = sel.target
    txt = "%s\n%.2f yds/att" % (sel.artist.get_label(), ypa)
    sel.annotation.set_text(txt)
    sel.annotation.get_bbox_patch().set(fc="white")


def plot_wks(rdap, wk_str, ctgy, teams):
    idx = RUSH_TYPES.index(ctgy)
    if "-" in wk_str:
        start, stop = list(map(lambda x: int(x), wk_str.split("-")))
        wks = range(start - 1, stop)
    else:
        wks = [int(wk_str) - 1]
    pts = []
    for team in teams:
        for wk in wks:
            # skip bye week
            if rdap[team][wk] is None:
                continue
            wk_data = list(rdap[team][wk])
            y, x = subgroup(wk_data, 2)[idx]
            c = TEAM_COLORS[team].primary
            ec = TEAM_COLORS[team].secondary
            label = "(Week %d)\n%s" % (wk + 1, team)
            p = plt.scatter(x, y, c=c, edgecolors=ec, linewidth=1, label=label)
            pts.append(p)
    plt.xlabel("Attempts")
    plt.ylabel("Yards")
    team_str = ", ".join(teams) if len(teams) <= 3 else "Team"
    plt.title("Yards per %s Attempt by %s (Week %s)"
              % (ctgy.upper(), team_str, wk_str))
    mplcursors.cursor(hover=True).connect("add", configure_popup)
    plt.show()


def plot_avgs(rdap, ctgy, teams):
    idx = RUSH_TYPES.index(ctgy)
    pts = []
    for team in teams:
        for wk in range(17):
            if rdap[team][wk] is None:
                continue
            wk_data = list(rdap[team][wk])
            y, x = subgroup(wk_data, 2)[idx]
            if x <= 0:
                continue  # ignore weeks with no attempts
            ypa = y / x
            c = TEAM_COLORS[team].primary
            ec = TEAM_COLORS[team].secondary
            label = "%s" % team
            p = plt.scatter(wk, ypa, c=c, edgecolors=ec, linewidth=1,
                            label=label)
            pts.append(p)
    plt.xlabel("Week")
    plt.ylabel("Yards per Attempt")
    team_str = ", ".join(teams) if len(teams) <= 3 else "Team"
    plt.title("Yards per Attempt per Week by %s" % team_str)
    mplcursors.cursor(hover=True).connect("add", configure_popup_avg)
    plt.show()


pp = PrettyPrinter(width=100)

parser = argparse.ArgumentParser(description="Visualize defensive efficacies")
parser.add_argument("ctgy", metavar="ctgy", type=str, nargs=1,
                    help='The category to analyze')
parser.add_argument("teams", metavar="teams", type=str, nargs="*",
                    default=TEAM_NAMES,
                    help="The specific teams to analyze")
parser.add_argument("--weeks", dest="wks", type=str, nargs=1,
                    help=("The range of weeks to analyze. If no value is "
                          "provided, will apply an average instead."))
args = parser.parse_args()

file = open("%s/rush_def_avgs_partial.pkl" % EFF_PKL_DIR, "rb")
rdap = pickle.load(file)
file.close()
if args.wks is not None:
    plot_wks(rdap, args.wks[0], args.ctgy[0], args.teams)
else:
    plot_avgs(rdap, args.ctgy[0], args.teams)
