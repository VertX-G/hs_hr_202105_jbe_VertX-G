from flask import Flask
import sqlite3

app = Flask(__name__)
DATABASE = '/db/assignment.sqlite3'

def get_db():
    db = getattr(g, '_database', None)

@app.route("/")
def home():
    return "Hello, Flask!"
