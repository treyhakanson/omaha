import sqlite3
from constants import DB_PATH

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()
c.execute("""
    SELECT player_link
        FROM player
""")
player_links = list(map(lambda x: x[0], c.fetchall()))
for pl in player_links:
    c.execute("""
        SELECT *
            FROM pass_tckl
            WHERE player_link = ?
    """, [pl])
    res = c.fetchall()
    if len(res) > 0:
        print(res)
        break
