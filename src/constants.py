'''
This file contains constants that are universal across scripts. Scripts may
also contain their own, more specific, constants.
'''
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

# Path to database file
DB_PATH = "../boxscore-data/db.sqlite"

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
