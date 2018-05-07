import os
import csv

FILE_DIR = "../boxscore-data/snap_counts"
OUTPUT_FILE = "../raw/misc/player-links.txt"
player_links = set()

for fname in os.listdir(FILE_DIR):
    with open("%s/%s" % (FILE_DIR, fname), "r") as file:
        reader = csv.reader(file)
        next(reader, None)
        for row in reader:
            player_links.add(row[1])

with open(OUTPUT_FILE, "w") as file:
    for player_link in player_links:
        file.write("%s\n" % player_link)
