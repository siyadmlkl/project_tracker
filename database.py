import sqlite3 as sqlt

with sqlt.connect('data.db') as conn:
    conn.row_factory = sqlt.Row
    cur = conn.cursor()
    cur.execute("DELETE FROM works WHERE id=21")
    works = cur.execute("SELECT * FROM works").fetchall()
    for cont in works:
        print(cont['id'])