# NFL Data Crawl and Analysis

## Overview

Repository to project and visualize player performance based on historical data.

## Usage

To retrieve, parse, and process boxscore data:

```sh
bash get-weeks.sh              # get weekly schedules
python3 get-boxscore-links.py  # get links to boxscores from schedules
bash get-boxscores.sh          # retrieve boxscores
python3 parse-boxscores.py     # parse/post-processing data from boxscores
```

To do the same for injury data:

```sh
bash get-injuries.sh       # retrieve raw injury pages
python3 parse-injuries.py  # parse/post-process injury pages
```

And for players:

```sh
python3 get-player-links.py
bash get-players.sh
python3 parse-players.py
```

To populate the sqlite3 database with the CSV data:

```sh
python3 populate-db.py
```

Note that the tables in the database may have some additional columns to aid in joining tables. For example, some tables feature a game column so that offensive and defensive players from the same game can be compared.
