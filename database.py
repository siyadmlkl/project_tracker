import sqlite3 as sqlt

with sqlt.connect('data.db') as conn:
    conn.row_factory = sqlt.Row
    cur = conn.cursor()

    cur.execute("DELETE FROM contractors WHERE id=8")
    items = cur.execute("SELECT * FROM contractors").fetchall()

    #cur.execute("DELETE FROM works WHERE id=21")
    #items = cur.execute("SELECT * FROM works").fetchall()

    for item in items:
        print(item['id'])