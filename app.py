from flask import Flask, render_template, request, redirect
import os
import sqlite3 as sqlt
import datetime

app = Flask(__name__)


def fetch_all_contractors():
    '''
    function used to fetch all contractors
    '''

    with sqlt.connect('data.db') as conn:
        conn.row_factory = sqlt.Row
        cur = conn.cursor()
        contractors = cur.execute("SELECT * FROM contractors").fetchall()
        return contractors

def fetch_all_works():
    '''
    Function used to fetch list of contractors and details
    '''
    with sqlt.connect('data.db') as conn:
        conn.row_factory = sqlt.Row
        cur=conn.cursor()
        works = cur.execute("SELECT contractor, location, \
                            comp_date,job_no, name, color, status,\
                            start_date FROM works \
                            INNER JOIN contractors on \
                            contractors.id=works.contractor\
                            WHERE status!='closed' ORDER BY contractor").fetchall()
        return works

def fetch_a_work(job,number):
    '''
    search and return work/s based on condition
    '''
    query = f"SELECT contractor, location, \
                        comp_date,job_no, name, color, status,\
                        start_date FROM works \
                        INNER JOIN contractors on \
                        contractors.id=works.contractor \
                            WHERE {job}='{number}'"
    with sqlt.connect('data.db') as conn:
        conn.row_factory = sqlt.Row
        cur = conn.cursor()
        works = cur.execute(query).fetchall()
    return works


@app.route("/")
def home():
    '''
    View for home page
    '''
    works = fetch_all_works()
    today = int(datetime.datetime.strftime(datetime.date.today(), "%Y%m%d"))
    context = {"works": works,
               "today": today}
    return render_template('index.html', **context)


@app.route("/contractors", methods=('GET','POST'))
def contractor():
    '''
    view for contractors page
    '''
    if request.method=='POST':
        name_ = request.form['name']
        color = request.form['color']
        coc=''
        if 'coc' in request.form:
            coc=True
        else:
            coc=False

        with sqlt.connect('data.db') as conn:
            conn.row_factory = sqlt.Row
            cur = conn.cursor()
            query = f"INSERT INTO contractors(name,color,coc) VALUES('{name_}','{color}',{coc})"
            cur.execute(query)
            conn.commit()

        contractors = fetch_all_contractors()
        context = {"contractors": contractors}
        return render_template('contractors.html', **context)


    contractors = fetch_all_contractors()
    context = {"contractors": contractors}
    return render_template('contractors.html', **context)


@app.route("/add_project", methods=('GET', 'POST'))
def add_project():
    '''
    View for add project page(get, post)
    '''
    if request.method == 'POST':
        _contractor = request.form['name']
        location = request.form['location']
        job_no = request.form['job_no']
        start_date = request.form['start_date']
        comp_date = request.form['comp_date']

        with sqlt.connect('data.db') as conn:
            conn.row_factory = sqlt.Row
            cur = conn.cursor()
            cur.execute('INSERT INTO works(contractor,location,job_no,start_date,comp_date, status)\
                    VALUES(?,?,?,?,?,?)', (_contractor, location,
                        job_no, start_date, comp_date, "Ongoing"))
            conn.commit()
            return redirect('/')

    contractors = fetch_all_contractors()
    context = {"contractors": contractors}
    return render_template('addproject.html', **context)


@app.route("/edit", methods=('GET', 'POST'))
def edit_project():
    '''
    view for edit project page(get, post)
    '''
    job_no = str(request.args.get('job'))
    if request.method=='POST':
        status = request.form['status']
        with sqlt.connect('data.db') as conn:
            conn.row_factory = sqlt.Row
            cur = conn.cursor()
            query = f"UPDATE works SET status='{status}' WHERE job_no='{job_no}'"
            cur.execute(query)
            conn.commit()
        return redirect('/')

    works = fetch_a_work("job_no",job_no)

    today = int(datetime.datetime.strftime(datetime.date.today(), "%Y%m%d"))
  
    print("job - ",job_no+'1')
    context = {"works": works,
               "today": today}

    return render_template('editwo.html',**context)

@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == "__main__":
    app.run(debug=True)
    #app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
