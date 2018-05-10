# NFL Data Crawl and Analysis

## Overview

Repository to project and visualize player performance based on historical data.

## Available Data

* `boxscore-data` contains parsed components of boxscore data in CSV format
* `injuries` contains injury week by week injury
* `boxscore-data/db.sqlite` a sqlite3 format of all the repository's CSV data

## Basic Setup

Before cloning, create and activate a virtual environment using `venv`, **NOT** `virtualenv`, to ensure plotting libraries function properly:

```sh
python3 -m venv omaha-env       # create virtual environment
source omaha-env/bin/activate  # activate virtual environment
```

Then, clone the repository inside `omaha-env` and install the required dependencies:

```sh
pip install -r requirements.txt  # from ./omaha-env/omaha
```

## Retrieval and Processing

This section pertains to retrieval and processing of the data. All data come with the repository and will be periodically updated, but in the case that additional data is desired/required the pipeline is as follows:

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

And for players (requires processed boxscore data):

```sh
python3 get-player-links.py  # retrieve unique player links from snap counts
bash get-players.sh          # retrieves raw player pages
python3 parse-players.py     # parse/post-process player pages (combine data)
```

To populate the sqlite3 database with the CSV data:

```sh
python3 populate-db.py  # requires all of above data to populate db
```

Note that the tables in the database may have some additional columns to aid in joining tables. For example, some tables feature a game column so that offensive and defensive players from the same game can be compared.
