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

To get injury data:

```sh
bash get-injuries.sh       # retrieve raw injury pages
python3 parse-injuries.py  # parse/post-process injury pages
```
