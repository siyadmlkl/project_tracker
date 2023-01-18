from flask import Flask, render_template, request, flash, redirect
import os
import sqlite3
import datetime

app = Flask(__name__)

conn = sqlite3.connect('data.db',check_same_thread=False)
conn.row_factory=sqlite3.Row


def fetchAllContractors():
    cur = conn.cursor()
    contractors = cur.execute("SELECT * FROM contractors").fetchall()
    return contractors

def fetchAllWorks():
    cur = conn.cursor()
    works = cur.execute("SELECT contractor, location, \
                        comp_date,job_no, name, color, status,\
                        start_date FROM works \
                        INNER JOIN contractors on \
                        contractors.id=works.contractor\
                        WHERE status!='closed' ORDER BY contractor").fetchall()
    return works



@app.route("/")
def home():
    works = fetchAllWorks()
    today = int(datetime.datetime.strftime(datetime.date.today(),"%Y%m%d"))
    context={"works":works,
                "today":today}
    return render_template('index.html', **context)

@app.route("/contractors")
def contractor():
    contractors = fetchAllContractors()
    context={"contractors":contractors}
    return render_template('contractors.html', **context)

@app.route("/addproject", methods=('GET','POST'))
def addProject():
    if request.method == 'POST':
        contractor=request.form['name']
        location=request.form['location']
        job_no=request.form['job_no']
        start_date=request.form['start_date']
        comp_date=request.form['comp_date']

        cur = conn.cursor()
        cur.execute('INSERT INTO works(contractor,location,job_no,start_date,comp_date, status)\
                VALUES(?,?,?,?,?,?)',(contractor,location,\
                    job_no,start_date,comp_date,"ongoing"))
        conn.commit()

        return redirect('/')
    contractors = fetchAllContractors()
    context = {"contractors":contractors}
    return render_template('addproject.html',**context)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))