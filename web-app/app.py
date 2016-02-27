import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from contextlib import closing


DATABASE = '/tmp/yaks.db'
DEBUG = True
SECRET_KEY = 'gobears'
USERNAME = 'berkeley'
PASSWORD = 'boardreview'


app = Flask(__name__)
app.config.from_object(__name__)

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    print("hello")
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

@app.route('/')
def home():
  init_db()
  connect_db().text_factory = str
  return render_template('home.html')

if __name__ == '__main__':
    app.run(debug = True)