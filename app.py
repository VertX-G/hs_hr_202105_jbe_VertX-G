import sqlite3
from flask import Flask, g
from flask.templating import render_template

# Pure SQLite
#https://docs.python.org/3/library/sqlite3.html

#con = sqlite3.connect('db/assignment.sqlite3')



# SQLite 3 with Flask
# https://flask.palletsprojects.com/en/2.0.x/patterns/sqlite3/


DATABASE = 'db/assignment.sqlite3'

'''Configure application'''
app = Flask(__name__)

'''Ensure templates are auto-reloaded'''
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

@app.route("/")
def login():
    cur = get_db().cursor()
    #cur.execute('SELECT * FROM user')
    #users = cur.fetchall()
    users = cur.execute('SELECT * FROM user')
    return render_template('login.html', users = users)    
