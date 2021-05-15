import sqlite3
from flask import Flask, g, redirect, render_template, request, session
from flask_session import Session
import hashlib
#from passlib.hash import sha256_crypt

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

# TODO def log_login():
#   check if table exists
#   if exists, add entry
#   else create table and add entry

#   table to use foreign key from user

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
    users = cur.execute('SELECT * FROM user WHERE username = ?', [session['username']]) #("SELECT * FROM user WHERE username = ?", request.form.get("username"))
    print(f'users: {users}')
    #print(f'users: {users["firstname"]}')

    return render_template('test_index.html', users = users)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username_attempt = request.form.get("username")
        password_attempt = hashlib.sha256(request.form.get("password").encode()).hexdigest()
        print(f'Username Attempt: {username_attempt}')
        print(f'Password Attempt: {password_attempt}')

        cur = get_db().cursor()
        #user_check = cur.execute('SELECT * FROM user WHERE username = ?', [user_attempt]).fetchone()
        #user_exists = cur.execute('SELECT username, firstname, lastname, isadmin FROM user WHERE username = ? AND password = ? LIMIT 1', [username_attempt, password_attempt]).fetchone()
        #TODO basic authentication
        user_exists = cur.execute('SELECT username, firstname, lastname, password, isadmin FROM user WHERE username = ? LIMIT 1', [username_attempt]).fetchone()
        #print(user_check)
        if user_exists:
            if password_attempt == user_exists['password']:
                print(user_exists['firstname'])
                session['username'] = user_exists['username']
                session['firstname'] = user_exists['firstname']
                session['lastname'] = user_exists['lastname']
                session['isadmin'] = user_exists['isadmin']
                session['last_login_datetime']
                #log_login()
                return redirect('/')
            # log_login()
        # write incorrect username or password
    return render_template('login.html')
"""
    cur = get_db().cursor()
    #cur.execute('SELECT * FROM user')
    #users = cur.fetchall()
    users = cur.execute('SELECT * FROM user')
    return render_template('login.html', users = users)
"""
"""
@app.route('/log')
def index():
    if not session.get('isadmin'):
        return redirect('/login')

    # FIX THESE
    cur = get_db().cursor()
    #cur.execute('SELECT * FROM user')
    #users = cur.fetchall()
    users = cur.execute('SELECT * FROM user WHERE username = ?', [session['username']]) #("SELECT * FROM user WHERE username = ?", request.form.get("username"))
    print(f'users: {users}')
    #print(f'users: {users["firstname"]}')

    return render_template('log.html', users = users)
"""

@app.route('/logout')   
def logout():
    #session['username'] = None #else need to add all other session variables
    session.clear()
    return redirect('/')