"""
This file contains constants that are universal across scripts. Scripts may
also contain their own, more specific, constants.
"""

# full team names
TEAM_NAMES = ["Arizona Cardinals",
              "Atlanta Falcons",
              "Baltimore Ravens",
              "Buffalo Bills",
              "Carolina Panthers",
              "Chicago Bears",
              "Cincinnati Bengals",
              "Cleveland Browns",
              "Dallas Cowboys",
              "Denver Broncos",
              "Detroit Lions",
              "Green Bay Packers",
              "Houston Texans",
              "Indianapolis Colts",
              "Jacksonville Jaguars",
              "Kansas City Chiefs",
              "Los Angeles Chargers",
              "Los Angeles Rams",
              "Miami Dolphins",
              "Minnesota Vikings",
              "New England Patriots",
              "New Orleans Saints",
              "New York Giants",
              "New York Jets",
              "Oakland Raiders",
              "Philadelphia Eagles",
              "Pittsburgh Steelers",
              "San Francisco 49ers",
              "Seattle Seahawks",
              "Tampa Bay Buccaneers",
              "Tennessee Titans",
              "Washington Redskins"]


# primary team colors (for plotting purposes)
class TeamColor:
    def __init__(self, primary, secondary):
        self.primary = primary
        self.secondary = secondary


TEAM_COLORS = {
    "Arizona Cardinals": TeamColor((0.61, 0.15, 0.26), (1.00, 0.80, 0.00)),
    "Atlanta Falcons": TeamColor((0.65, 0.10, 0.18), (0.00, 0.00, 0.00)),
    "Baltimore Ravens": TeamColor((0.14, 0.09, 0.45), (0.00, 0.00, 0.00)),
    "Buffalo Bills": TeamColor((0.78, 0.06, 0.18), (0.00, 0.20, 0.55)),
    "Carolina Panthers": TeamColor((0.00, 0.52, 0.79), (0.00, 0.00, 0.00)),
    "Chicago Bears": TeamColor((0.02, 0.11, 0.17), (0.86, 0.27, 0.02)),
    "Cincinnati Bengals": TeamColor((0.99, 0.30, 0.01), (0.06, 0.09, 0.13)),
    "Cleveland Browns": TeamColor((0.92, 0.20, 0.00), (0.22, 0.18, 0.18)),
    "Dallas Cowboys": TeamColor((0.02, 0.12, 0.26), (0.53, 0.58, 0.59)),
    "Denver Broncos": TeamColor((0.05, 0.14, 0.25), (0.99, 0.30, 0.01)),
    "Detroit Lions": TeamColor((0.00, 0.41, 0.69), (0.64, 0.67, 0.68)),
    "Green Bay Packers": TeamColor((0.09, 0.19, 0.16), (1.00, 0.72, 0.11)),
    "Houston Texans": TeamColor((0.04, 0.12, 0.17), (0.65, 0.10, 0.18)),
    "Indianapolis Colts": TeamColor((0.00, 0.23, 0.44), (0.00, 0.23, 0.44)),
    "Jacksonville Jaguars": TeamColor((0.00, 0.38, 0.45), (0.83, 0.62, 0.07)),
    "Kansas City Chiefs": TeamColor((0.78, 0.06, 0.18), (1.00, 0.72, 0.11)),
    "Los Angeles Chargers": TeamColor((0.05, 0.14, 0.25), (1.00, 0.72, 0.11)),
    "Los Angeles Rams": TeamColor((0.00, 0.13, 0.27), (0.00, 0.13, 0.27)),
    "Miami Dolphins": TeamColor((0.00, 0.56, 0.59), (0.96, 0.51, 0.13)),
    "Minnesota Vikings": TeamColor((0.32, 0.18, 0.43), (1.00, 0.72, 0.11)),
    "New England Patriots": TeamColor((0.05, 0.14, 0.25), (0.78, 0.06, 0.18)),
    "New Orleans Saints": TeamColor((0.64, 0.55, 0.36), (0.00, 0.00, 0.00)),
    "New York Giants": TeamColor((0.00, 0.12, 0.38), (0.65, 0.10, 0.18)),
    "New York Jets": TeamColor((0.05, 0.22, 0.11), (0.05, 0.22, 0.11)),
    "Oakland Raiders": TeamColor((0.65, 0.67, 0.69), (0.00, 0.00, 0.00)),
    "Philadelphia Eagles": TeamColor((0.02, 0.30, 0.33), (0.44, 0.50, 0.56)),
    "Pittsburgh Steelers": TeamColor((0.00, 0.00, 0.00), (1.00, 0.72, 0.11)),
    "San Francisco 49ers": TeamColor((0.61, 0.15, 0.26), (0.54, 0.42, 0.30)),
    "Seattle Seahawks": TeamColor((0.00, 0.08, 0.20), (0.30, 1.00, 0.00)),
    "Tampa Bay Buccaneers": TeamColor((0.78, 0.06, 0.18), (0.24, 0.22, 0.21)),
    "Tennessee Titans": TeamColor((0.05, 0.14, 0.25), (0.29, 0.57, 0.86)),
    "Washington Redskins": TeamColor((0.53, 0.15, 0.20), (1.00, 0.80, 0.00))
}

# Path to database file
DB_PATH = "../db.sqlite"

# Path to efficacy pickles
EFF_PKL_DIR = "../efficacies/pickles"

# Passing information
PASS_GEN_TYPES = ["cmp", "att", "yds", "td", "int", "sk"]

# Route information
ROUTE_TYPES = ["short_l",
               "short_mid",
               "short_r",
               "deep_l",
               "deep_mid",
               "deep_r"]
ROUTE_ATTRS = ["tgt", "ctch", "yds", "td"]

# Rush information
RUSH_TYPES = ["l_end",
              "l_tckl",
              "l_guard",
              "mid",
              "r_guard",
              "r_tckl",
              "r_end"]
RUSH_ATTRS = ["att", "yds", "td"]

# Defensive information
PASS_TCKL_TYPES = ["short_r",
                   "short_mid",
                   "short_l",
                   "deep_r",
                   "deep_mid",
                   "deep_l"]
TCKL_ATTRS = ["tckl", "dfnd"]

# Snap count information
SNAP_COUNT_TYPES = ["off", "def", "st"]
SNAP_COUNT_ATTRS = ["num", "pct"]
SNAP_COUNT_PRE_COLS = ["pos"]

# Defensive positions
DEF_POS = ["CB", "FS", "LB", "SS", "DE", "DT", "NT", "DB", "S"]  # All
DLINE_POS = ["DE", "DT", "NT"]  # Defensive line
SEC_POS = ["CB", "FS", "SS", "DB", "S"]  # Secondary

# Offensive positions
OFF_POS = ["T", "G", "QB", "C", "RB", "WR", "TE", "FB"]
QB_POS = "QB"  # Quarterback
OLINE_POS = ["T", "G", "C"]  # Offensive line
REC_POS = ["WR", "TE"]  # Primary receivers
BACK_POS = ["RB", "FB"]  # Halfbacks (primary rushers)

# Special teams positions (only those _specific_ to special teams; many
# offensive and defensive positions will also appear on special teams)
ST_POS = ["K", "P", "LS"]
KICK_POS = "K"  # Kicker

# All positions
ALL_POS = [*DEF_POS, *OFF_POS, *ST_POS]
