import os
import csv
import sqlite3

DB_PATH = "../boxscore-data/db.sqlite"
TABLE_NAMES = ["pass_tckl", "tgt_dir"]
TABLE_DIR = {
    "pass_tckl": "../boxscore-data/pass_tckls",
    "tgt_dir": "../boxscore-data/tgt_dirs"
}
TABLE_QUERY = {
    "pass_tckl": """
        INSERT INTO pass_tckl
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """,
    "tgt_dir": """
        INSERT INTO tgt_dir
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                ?, ?, ?, ?, ?, ?, ?)
    """
}
ROW_MUTATION = {
    "pass_tckl": lambda row, fname: [*row[0:2], fname, *row[2:]],
    "tgt_dir": lambda row, fname: [*row[0:2], fname, *row[2:]]
}

conn = sqlite3.connect(DB_PATH)
for tn in TABLE_NAMES:
    conn.execute("DELETE FROM %s" % tn)


def upload_data(query, file_dir, mutation):
    for fname in os.listdir(file_dir):
        with open("%s/%s" % (file_dir, fname), "r") as file:
            reader = csv.reader(file)
            next(reader, None)
            data = [mutation(row, fname) for row in reader]
            conn.executemany(query, data)


for tn in TABLE_NAMES:
    print("Uploading data for %s..." % tn)
    upload_data(TABLE_QUERY[tn], TABLE_DIR[tn], ROW_MUTATION[tn])

conn.commit()
conn.close()
print("Done.")
