import sqlite3
from flask import Flask, g, redirect, render_template, request, session
from flask_session import Session
import hashlib
from datetime import datetime

# from passlib.hash import sha256_crypt


"""Configure application"""
app = Flask(__name__)

"""Configure sessions"""
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

"""Ensure templates are auto-reloaded"""
app.config["TEMPLATES_AUTO_RELOAD"] = True

"""Assign database file"""
DATABASE = "db/assignment.sqlite3"


"""Configure database usage"""


def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)

    db.row_factory = sqlite3.Row
    return db


"""log login attempts function"""


def log_login(user_id, login_success):

    cur = get_db().cursor()
    """
    cur.execute(
        "CREATE TABLE IF NOT EXISTS login_log (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, login_success INTEGER NOT NULL, log_time TEXT NOT NULL, user_id INTEGER NOT NULL, FOREIGN KEY (user_id) REFERENCES user(id))"
    )
    """
    cur.execute(
        'INSERT INTO login_log(login_success, log_time, user_id) VALUES (?, datetime("now"), ?)',
        [login_success, user_id],
    )

    get_db().commit()


"""Close database when app closes"""


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()


@app.route("/")
def index():
    """only access index.html if a valid session is in progress"""
    if not session.get("username"):
        return redirect("/login")

    # cur = get_db().cursor()
    # cur.execute("SELECT * FROM user")

    # users = cur.fetchall()
    # users = cur.execute('SELECT * FROM user WHERE username = ?', [session['username']]) #("SELECT * FROM user WHERE username = ?", request.form.get("username"))
    # print(f'users: {users}')
    # print(f'users: {users["firstname"]}')

    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        """Get username from form"""
        username_attempt = request.form.get("username")
        """Get password from form and hash it"""
        password_attempt = hashlib.sha256(
            request.form.get("password").encode()
        ).hexdigest()
        # print(f"Username Attempt: {username_attempt}")
        # print(f"Password Attempt: {password_attempt}")

        """Create login_log table if it doesnt exist"""
        cur = get_db().cursor()
        cur.execute(
            "CREATE TABLE IF NOT EXISTS login_log (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, login_success INTEGER NOT NULL, log_time TEXT NOT NULL, user_id INTEGER NOT NULL, FOREIGN KEY (user_id) REFERENCES user(id))"
        )

        """Check if username exists in database"""
        # TODO basic authentication
        user_exists = cur.execute(
            "SELECT * FROM user WHERE username = ?", [username_attempt]
        ).fetchone()
        # user_check = cur.execute('SELECT * FROM user WHERE username = ?', [user_attempt]).fetchone()
        # user_exists = cur.execute('SELECT username, firstname, lastname, isadmin FROM user WHERE username = ? AND password = ? LIMIT 1', [username_attempt, password_attempt]).fetchone()
        if user_exists:
            """Check password"""
            if password_attempt == user_exists["password"]:
                """Grab the rest of the user's data for the session"""
                session["id"] = user_exists["id"]
                session["username"] = user_exists["username"]
                session["firstname"] = user_exists["firstname"]
                session["lastname"] = user_exists["lastname"]
                session["isadmin"] = user_exists["isadmin"]

                """
                session["last_login"] = cur.execute(
                    "SELECT log_time FROM login_log WHERE user_id = ? ORDER BY log_time DESC LIMIT 1",
                    [user_exists["id"]],
                ).fetchone()["log_time"]
                """
                """Check last login"""
                last_login = cur.execute(
                    "SELECT log_time FROM login_log WHERE user_id = ? ORDER BY log_time DESC LIMIT 1",
                    [user_exists["id"]],
                ).fetchone()

                if last_login:
                    """Get last login time"""
                    session["last_login"] = last_login["log_time"]
                    # print(f"last login: {session['last_login']}")

                    """Count failed logins"""
                    session["failed_logins"] = cur.execute(
                        "SELECT COUNT(*) FROM login_log WHERE user_id = ? AND login_success = 0",  # TODO only count failed logins after last successful login
                        [user_exists["id"]],
                    ).fetchone()["COUNT(*)"]
                    # print(f"number of failed logins: {session['failed_logins']}")

                # session['last_login_datetime']
                """Log successfull login"""
                log_login(user_exists["id"], 1)
                return redirect("/")
            """Log failed login"""
            log_login(user_exists["id"], 0)
    return render_template("login.html")


"""
    cur = get_db().cursor()
    #cur.execute('SELECT * FROM user')
    #users = cur.fetchall()
    users = cur.execute('SELECT * FROM user')
    return render_template('login.html', users = users)
"""


@app.route("/log")
def log():
    """Only give access to user with admin privileges"""
    if not session.get("isadmin"):
        return redirect("/login")

    """Get all login logs"""
    cur = get_db().cursor()
    logs = cur.execute(
        "SELECT login_log.log_time, login_log.login_success, user.username, user.firstname, user.lastname FROM login_log INNER JOIN user ON login_log.user_id = user.id ORDER BY log_time DESC"
    ).fetchall()
    return render_template("log.html", logs=logs)


"""Logout and clear session"""


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")
