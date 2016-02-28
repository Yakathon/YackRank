import sqlite3
import nltk
import itertools
import operator
from readability.readability import Readability
from readability import utils



def common_dicts():
    con = sqlite3.connect('yaks.db')
    cur = con.cursor()
    con.text_factory = str
    cdict = {}
    cur.execute("""SELECT * FROM raw_yaks""")
    rows = cur.fetchall()
    for row in rows:
        cid = row[1]
        if cid not in cdict.keys():
            cdict[cid] = [row[2].lower()]
        else:
            cdict[cid].append(row[2].lower())
    con.close()
    return cdict


def common_words_algorithm():
    cdict = common_dicts()
    word_dict = {}
    for college in cdict.keys():
        all_words = ' '.join(cdict[college])
        cword = common_word(all_words)
        word_dict[college] = cword
    return word_dict

def populateValuableWordsDB():
    con = sqlite3.connect('yaks.db')
    cur = con.cursor()
    con.text_factory = str
    cur.execute('DELETE FROM most_valuable_words')

    word_dict = common_words_algorithm()
    for i in word_dict.items():
        cur.execute('INSERT INTO most_valuable_words (college_id, word_text) VALUES (?,?)', i)
    con.commit()
    con.close()


def common_word(all_words):
    s = set(nltk.corpus.stopwords.words('english'))
    t = {'like', 'people'}
    tokens = filter(lambda elem: len(elem) > 3 and elem not in s and elem not in t, nltk.word_tokenize(all_words))
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

def populateTopYaksDB():
    con = sqlite3.connect('yaks.db')
    cur = con.cursor()
    con.text_factory = str
    print("populating")
    topyaks = getTopYaks()
    cur.executemany('INSERT INTO top_yaks (college_id, yak_text) VALUES (?,?)', topyaks.items())
    con.commit()
    con.close()

#TODO: NEEDS TO CREATE ADD TO DATABASE
def getTopYaks():
    con = sqlite3.connect('yaks.db')
    cur = con.cursor()
    con.text_factory = str
    print("getting top yaks")
    cur.execute("SELECT c.college_id, c.name, y.yak_text, y.upvotes FROM raw_yaks as y, colleges as c WHERE c.college_id = y.college_id GROUP BY y.college_id ORDER BY y.upvotes;")
    yaks = cur.fetchall()
    top_yaks = {}
    for yak in yaks:
        print(yak)
        top_yaks[yak[0]] = yak[2]
    con.close()
    return top_yaks


def populateReadabilityTables():
    con = sqlite3.connect('yaks.db')
    cur = con.cursor()
    con.text_factory = str
    cur.execute('DELETE FROM college_readability;')
    cur.execute('DELETE FROM college_grade_level;')
    cdict = common_dicts()
    grades = {}
    readabilities = {}
    for college in cdict.keys():
        readabilities_arr = []
        grades_arr = []
        for yak in cdict[college]:
            readability, grade = getReadabilities(yak)
            readabilities_arr.append(readability)
            grades_arr.append(grade)
        readabilities[college] = sum(readabilities_arr)/len(readabilities_arr)
        grades[college] = sum(grades_arr)/len(grades_arr)
    print("!!!!!!!!!", readabilities)
    print(grades, "!!!!!!!!!!!!")
    cur.executemany('INSERT INTO college_readability (college_id, average_readability) VALUES (?,?);', readabilities.items())
    con.commit()
    cur.executemany('INSERT INTO college_grade_level (college_id, average_grade_level) VALUES (?,?);', grades.items())
    con.commit()
    con.close()


def populateTimesSwore():
    con = sqlite3.connect('yaks.db')
    cur = con.cursor()
    con.text_factory = str
    cur.execute('DELETE FROM times_swore')

    num_sworn = num_swear_algorithm()
    for i in num_sworn.items():
        cur.execute('INSERT INTO times_swore (college_id, times_swore) VALUES (?,?)', i)
    con.commit()
    con.close()


def getReadabilities(string):
    read = Readability(string)
    return read.FleschReadingEase(), read.FleschKincaidGradeLevel()
    

def num_swear_algorithm():
    swear_dict = {}
    sdict = group_colleges()
    for college in sdict.keys():
        all_words = ' '.join(sdict[college])
        swears = num_swears(all_words)
        swear_dict[college] = swears
    return swear_dict


def num_swears(words):
    s = {'fuck', 'bitch', 'asshole', 'ass', 'damn', 'hell', 'cunt', 'twat', 'fucker', 'fucking',
         'nigga', 'nigger', 'shit', 'shitty', 'pussy', 'blowjob', 'bj', 'dick', 'mofo', 'motherfucker'}
    swears = len(list(filter(lambda elem: elem in s, nltk.word_tokenize(words))))
    return swears


def test_print():
    print("Hello")
    colleges = cur.fetchall()
    for college in colleges:
        print(college[1])

populateValuableWordsDB()