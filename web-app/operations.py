import sqlite3
import nltk
import itertools
import operator

con = sqlite3.connect('yaks.db')
cur = con.cursor()
con.text_factory = str


def common_dicts():
    cdict = {}
    cur.execute("""SELECT * FROM raw_yaks""")
    rows = cur.fetchall()
    for row in rows:
        cid = row[1]
        if cid not in cdict.keys():
            cdict[cid] = [row[2]]
        else:
            cdict[cid].append(row[2])
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
    print(word_dict.items())
    cur.executemany('INSERT INTO most_valuable_words (college_id, word_text) VALUES (?,?)', word_dict.items())


def common_word(all_words):
    tokens = filter(lambda elem: len(elem) > 3, nltk.word_tokenize(all_words))
    return most_common_word_in_list(tokens)


# Shamelessly used from Stackoverflow user Hoju
def most_common_word_in_list(L):
    L = list(L)
    # get an iterable of (item, iterable) pairs
    SL = sorted((x, i) for i, x in enumerate(L))
    # print 'SL:', SL
    groups = itertools.groupby(SL, key=operator.itemgetter(0))
    # auxiliary function to get "quality" for an item
    def _auxfun(g):
        item, iterable = g
        count = 0
        min_index = len(L)
        for _, where in iterable:
            count += 1
            min_index = min(min_index, where)
        return count, -min_index
    return max(groups, key=_auxfun)[0]


def test_print():
    print("Hello")
    colleges = cur.fetchall()
    for college in colleges:
        print(college[1])

populate_db()
test_print()