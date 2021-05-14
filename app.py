import sqlite3
from flask import Flask, g, redirect, render_template, request, session
from flask_session import Session

# Pure SQLite
#https://docs.python.org/3/library/sqlite3.html

#con = sqlite3.connect('db/assignment.sqlite3')



# SQLite 3 with Flask
# https://flask.palletsprojects.com/en/2.0.x/patterns/sqlite3/


DATABASE = 'db/assignment.sqlite3'

"""Configure application"""
app = Flask(__name__)

"""Configure sessions"""
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

"""Ensure templates are auto-reloaded"""
app.config['TEMPLATES_AUTO_RELOAD'] = True

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    
    db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def index():
    if not session.get('username'):
        return redirect('/login')

    cur = get_db().cursor()
    #cur.execute('SELECT * FROM user')
    #users = cur.fetchall()
    users = cur.execute('SELECT * FROM user WHERE username = ?', (session['username'],)) #("SELECT * FROM user WHERE username = ?", request.form.get("username"))

    return render_template('test_index.html', users = users)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form.get('username')
        #username + password
        return redirect('/')
    return render_template('login.html')
"""
    cur = get_db().cursor()
    #cur.execute('SELECT * FROM user')
    #users = cur.fetchall()
    users = cur.execute('SELECT * FROM user')
    return render_template('login.html', users = users)
"""

@app.route('/logout')   
def logout():
    session['username'] = None
    return redirect('/')