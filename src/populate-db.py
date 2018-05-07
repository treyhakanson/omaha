import os
import csv
import sqlite3

DB_PATH = "../boxscore-data/db.sqlite"
TABLE_CONFIG = {
    "player": {
        "dir": "../boxscore-data/players",
        "query": """
            INSERT INTO player
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        "mutation": lambda row, fname: row
    },
    "pass_tckl": {
        "dir": "../boxscore-data/pass_tckls",
        "query": """
            INSERT INTO pass_tckl
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        "mutation": lambda row, fname: [*row[0:2], fname, *row[2:]]
    },
    "tgt_dir": {
        "dir": "../boxscore-data/tgt_dirs",
        "query": """
            INSERT INTO tgt_dir
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                    ?, ?, ?, ?, ?, ?, ?)
        """,
        "mutation": lambda row, fname: [*row[0:2], fname, *row[2:]]
    }
}

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()
c.execute("""
SELECT 'DROP TABLE ' || name || ';'
    FROM sqlite_master
    WHERE type = 'table';
""")
for drop_statement in list(map(lambda x: x[0], c.fetchall())):
    conn.execute(drop_statement)
with open("./create_db.sql", "r") as file:
    for create_statement in file.read().split('\n\n'):
        conn.execute(create_statement)


def upload_data(query, file_dir, mutation):
    for fname in os.listdir(file_dir):
        with open("%s/%s" % (file_dir, fname), "r") as file:
            reader = csv.reader(file)
            next(reader, None)
            data = [mutation(row, fname) for row in reader]
            conn.executemany(query, data)


for tn in TABLE_CONFIG.keys():
    print("Uploading data for %s..." % tn)
    upload_data(TABLE_CONFIG[tn]["query"], TABLE_CONFIG[tn]["dir"],
                TABLE_CONFIG[tn]["mutation"])

conn.commit()
conn.close()
print("Done.")
