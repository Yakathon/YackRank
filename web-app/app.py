import sqlite3
from yaklient import *
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, jsonify, send_from_directory
from flask_apscheduler import APScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from contextlib import closing
from threading import Thread
from word_operations import populateValuableWordsDB
from word_operations import populateTopYaksDB
<<<<<<< HEAD
=======
from word_operations import populateReadabilityTables
from json_converter import getJson
import os


>>>>>>> a18622cbf2dbd915c2179bab4d5e67d0818f4a20

DATABASE = 'yaks.db' # Our database
DEBUG = True
SECRET_KEY = 'gobears'
USERNAME = 'berkeley'
PASSWORD = 'boardreview'

class Config(object):
    JOBS = [
        {
            'id': 'updateYaks',
            'func': '__main__:updateYaks',
            'args': (),
            'trigger': 'interval',
            'minutes': 10
        }
    ]
            
    SCHEDULER_VIEWS_ENABLED = True

<<<<<<< HEAD
app = Flask(__name__)
app.config.from_object(Config())

app = Flask(__name__, static_folder='static')
app.config.from_object(__name__)

=======
app = Flask(__name__, static_folder='static')
app.config.from_object(__name__)
>>>>>>> a18622cbf2dbd915c2179bab4d5e67d0818f4a20

def connect_db():
    return sqlite3.connect("yaks.db")

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

#HELPER METHOD FOR POPULATE RAW YAKS
def insert(array, words):
    array.append((float(words[1]), float(words[2]), words[0]))

#GENERATE THE COLLEGES FROM "50notsuckyschools.txt"
def generateColleges(db):
    db.cursor().execute('DELETE FROM colleges')
    school_pos = []
    with open('lessthan50schools.txt') as f:
        for line in f:
            words = [i.strip() for i in line.split(',')]
            insert(school_pos, words)
    db.cursor().executemany('INSERT INTO colleges (latitude, longitude, name) VALUES (?,?,?)', school_pos)
    db.commit()

#HELPER METHOD FOR POPULATE RAW YAKS    
def addYaksFromCollege(location,college_id):
    db = connect_db()
    cur = db.cursor()
    user = User(location, "21C6CA60E3AA43C4B8C18B943394E111")
    yaks = user.get_yaks()
    for yak in yaks:
        if yak.score != None:
            try:
                cur.execute("INSERT INTO raw_yaks (college_id, yak_text, upvotes) VALUES (?,?,?)",(college_id,yak.message,yak.score))
            except:
                print("uh oh", yak)
            db.commit()

# PULL YAKS USING YAKLIENT
def populateRawYaks():
    db = connect_db()
    cur = db.cursor()
    cur.execute('DELETE FROM raw_yaks')
    db.commit()
    cur.execute("SELECT * FROM colleges")
    colleges = cur.fetchall()
    for college in colleges:
        print(college[3])
        college_id = college[0]
        lattitude = college[1]
        longitude = college[2]
        location = Location(lattitude,longitude)
        addYaksFromCollege(location, college_id)

def updateYaks():
    populateRawYaks()
    populateValuableWordsDB()
    populateTopYaksDB()
    populateReadabilityTables()


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
    db = connect_db()
    cur = db.cursor()
    
    cur.execute("SELECT * FROM top_yaks")
    yaks = cur.fetchall()
    print("printing yaks 1")
    for yak in yaks:
        print(yak)
    print("printed yaks")

    cur.execute("SELECT * FROM most_valuable_words")
    yaks = cur.fetchall()
    print("printing yaks 2")
    for yak in yaks:
        print(yak)
    print("printed yaks")
    return render_template('main.html')

    cur.execute("SELECT * FROM college_readability")
    yaks = cur.fetchall()
    print("printing yaks 3")
    for yak in yaks:
        print(yak)
    print("printed yaks")

    cur.execute("SELECT * FROM college_grade_level")
    yaks = cur.fetchall()
    print("printing yaks 4")
    for yak in yaks:
        print(yak)
    print("printed yaks")
    return render_template('main.html')

#@app.route('/index')

#@app.route('<filename>')
#def send_file(filename):  
    #print(filename)
    #return send_from_directory(app.static_folder, filename)
@app.route('/json', methods=['GET'])
def getStuff():
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "static", "data.json")
    data = json.load(open(json_url))
    print(data)
    return data

@app.route('/<path:filename>')
def serve_static(filename):
    root_dir = os.path.dirname(os.getcwd())
    return send_from_directory(os.path.join(root_dir, 'static', ''), filename)
# @app.route('/topwords')
# def topwords():


# @app.route('/top_yaks')
# def topwords():


if __name__ == '__main__':

    init_db()
    db = connect_db()
    db.text_factory = str
    #generates the colleges to pull yaks from
    print("Generating colleges")
    generateColleges(db)
    print("Generated colleges")
    #pulls initial set of yaks from each college
    print("Updating Yaks")
    updateYaks()
    print("Updated Yaks")
    
    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler.start()
    app.run(debug=False)


