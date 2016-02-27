import sqlite3
from yaklient import *
from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash
from contextlib import closing
from .operations import populate_db


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
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

def insert(array, words):
    array.append((float(words[1]), float(words[2]), words[0]))

def generateColleges(db):
    db.cursor().execute('DELETE FROM colleges')
    school_pos = []
    with open('50notsuckyschools.txt') as f:
        for line in f:
            words = [i.strip() for i in line.split(',')]
            insert(school_pos, words)
    db.cursor().executemany('INSERT INTO colleges (latitude, longitude, name) VALUES (?,?,?)', school_pos)
    db.commit()

def populateRawYaks(db):
    cur = db.cursor()
    cur.execute('DELETE FROM raw_yaks')
    db.commit()
    cur.execute("SELECT * FROM colleges")
    colleges = cur.fetchall()
    for college in colleges:
        college_id = college[0]
        lattitude = college[1]
        longitude = college[2]
        location = Location(lattitude,longitude)
        addYaksFromCollege(location, college_id)

def addYaksFromCollege(location,college_id):
    user = User(location, "21C6CA60E3AA43C4B8C18B943394E111")
    yaks = user.get_yaks()
    for yak in yaks:
        if yak.score != None:
            try:
                cur.execute("INSERT INTO raw_yaks (college_id, yak_text, upvotes) VALUES (?,?,?)",(college_id,yak.message,yak.score))
            except:
                print("uh oh", yak)
            con.commit()

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
    populateRawYaks(connect_db())
    populate_db()
    return render_template('home.html')

if __name__ == '__main__':
    init_db()
    db = connect_db()
    db.text_factory = str
    generateColleges(db)
    app.run(debug=True)
