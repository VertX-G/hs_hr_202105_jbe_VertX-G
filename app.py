import sqlite3
from flask import Flask, g, redirect, render_template, request, session, url_for
import hashlib
from datetime import datetime


# Configure application #
app = Flask(__name__)

# Configure sessions #
app.config["SESSION_PERMANENT"] = False
app.secret_key = "kL/20^:sZa9tEP$6WO`2T&J1yjBXA$"

# Ensure templates are auto-reloaded #
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Assign database file #
DATABASE = "db/assignment.sqlite3"


# Configure database usage #
def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)

    # Easier to use namedtuple rows #
    db.row_factory = sqlite3.Row
    return db


# log login attempts #
def log_login(user_id, login_success):
    cur = get_db().cursor()
    cur.execute(
        'INSERT INTO login_log(login_success, log_time, user_id) VALUES (?, datetime("now"), ?)',
        [login_success, user_id],
    )

    get_db().commit()


# Close database when app closes #
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()


# Protected page #
@app.route("/")
def index():

    # only access index.html if a valid session is in progress #
    if not session.get("username"):
        return redirect(url_for("login"))

    return render_template("index.html")


# Login #
@app.route("/login", methods=["GET", "POST"])
def login():
    cur = get_db().cursor()
    message = ""

    if request.method == "POST":

        # Get username from form #
        username_attempt = request.form.get("username")

        # Get password from form and hash it #
        password_attempt = hashlib.sha256(
            request.form.get("password").encode()
        ).hexdigest()

        # Check if username exists in database #
        user_exists = cur.execute(
            "SELECT * FROM user WHERE username = ?", [username_attempt]
        ).fetchone()

        if user_exists:

            # Create login_log table if it doesnt exist #
            cur.execute(
                "CREATE TABLE IF NOT EXISTS login_log (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, login_success INTEGER NOT NULL, log_time TEXT NOT NULL, user_id INTEGER NOT NULL, FOREIGN KEY (user_id) REFERENCES user(id))"
            )

            # Check password #
            if password_attempt == user_exists["password"]:

                # Grab the rest of the user's data for the session #
                session["id"] = user_exists["id"]
                session["username"] = user_exists["username"]
                session["firstname"] = user_exists["firstname"]
                session["lastname"] = user_exists["lastname"]
                session["isadmin"] = user_exists["isadmin"]

                # Check last login #
                last_login = cur.execute(
                    "SELECT log_time FROM login_log WHERE login_success = 1 AND user_id = ? ORDER BY log_time DESC LIMIT 1",
                    [user_exists["id"]],
                ).fetchone()

                if last_login:

                    # Get last login time #
                    session["last_login"] = datetime.strptime(
                        last_login["log_time"], "%Y-%m-%d %H:%M:%S"
                    )
                else:
                    session["last_login"] = 0

                # Count failed logins #
                session["failed_logins"] = cur.execute(
                    "SELECT COUNT(*) AS C FROM login_log WHERE login_success = 0 AND log_time > ? AND user_id = ?",
                    [session["last_login"], user_exists["id"]],
                ).fetchone()["C"]

                # Log successfull login #
                log_login(user_exists["id"], 1)
                return redirect(url_for("index"))

            # Log failed login #
            log_login(user_exists["id"], 0)

        # Failed login message #
        message = "Invalid username or password, please try again."

    # Logout message #
    if "logout" in request.args:
        message = "You have successfully logged out, see you soon."

    return render_template("login.html", message=message)


# Log page #
@app.route("/log")
def log():

    # Only give access to user with admin privileges #
    if not session.get("isadmin"):
        return redirect(url_for("login"))

    # Get all login logs #
    cur = get_db().cursor()
    logs = cur.execute(
        "SELECT login_log.log_time, login_log.login_success, user.username, user.firstname, user.lastname FROM login_log INNER JOIN user ON login_log.user_id = user.id ORDER BY log_time DESC"
    ).fetchall()
    return render_template("log.html", logs=logs)


# Logout and clear session #
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login", logout=1))
