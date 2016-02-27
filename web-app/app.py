import sqlite3
import nltk
from itertools import groupby as gg
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
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


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
  init_db()
  connect_db().text_factory = str
  return render_template('home.html')

if __name__ == '__main__':
    test_print()
    app.run(debug=True)
