# NFL Data Crawl and Analysis

To get boxscore data:

```sh
bash get-weeks.sh
python3 get-boxscore-links.py
bash get-boxscores.sh
python3 parse-boxscores.py
```

To get injury data:

```sh
bash get-injuries.sh
python3 parse-injuries.py
```
