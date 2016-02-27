import sqlite3
import nltk
from itertools import groupby as gg
from yaklient import *
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

def insert(array, words):
    print(words)
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
        print(college[3])
        location = Location(lattitude,longitude)
        print(location)
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

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = connect_db()
    return db


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


def common_dicts():
    cdict = {}
    for row in query_db('select * from raw_yaks group by college_id'):
        cid = row['college_id']
        if row[cid] not in cdict.keys():
            cdict[cid] = [row['word_text']]
        else:
            cdict[cid].append(row['word_text'])
    return cdict


def common_words_algorithm():
    cdict = common_dicts()
    word_dict = {}
    for college in cdict.keys():
        all_words = ' '.join(cdict[college])
        cword = common_word(all_words)
        word_dict[college] = cword
    return word_dict


def populate_db():
    word_dict = common_words_algorithm()
    conn = sqlite3.connect('flaskr.db')
    c = conn.cursor()
    c.executemany('INSERT INTO most_valuable_words (college_id, word_text) VALUES (?,?)', word_dict)


def common_word(all_words):
    tokens = filter(lambda elem: len(elem) > 3, nltk.word_tokenize(all_words))
    return most_common_word_in_list(tokens)


# Shamelessly used from Stackoverflow user Hoju
def most_common_word_in_list(L):
    return max(gg(sorted(L)), key=lambda x, v: (len(list(v)), -L.index(x)))[0]


def test_print():
    with app.app_context():
        print("Hello")
        for college in query_db('select * from most_valuable_words'):
            print(college['text'])


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
    return render_template('home.html')

if __name__ == '__main__':
    test_print()
    app.run(debug=True)

    init_db()
    db = connect_db()
    db.text_factory = str
    generateColleges(db)
    app.run(debug = True)
