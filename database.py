import sqlite3 as sqlt

conn=sqlt.connect('./data.db')
conn.row_factory=sqlt.Row

contractors = {}
works = {}

def fetchAllContractors():
    cur = conn.cursor()
    contractors = cur.execute("SELECT * FROM contractors").fetchall()
    conn.close
    return contractors


def fetchAllWorks():
    cur = conn.cursor()
    works = cur.execute("SELECT contractor, location, comp_date, name, color\
                        FROM works INNER JOIN contractors on \
                            contractors.id=works.contractor ORDER BY contractor").fetchall()
    conn.close
    return works

def insertProject(project):
    cur = conn.cursor()
    cur.execute('INSERT INTO works(contractor,location,comp_date)\
                VALUES(?,?,?)',(project['contractor'],\
                    project['location'],project['comp_date']))
    conn.commit()