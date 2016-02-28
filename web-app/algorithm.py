import sqlite3
import nltk
import itertools
import operator

con = sqlite3.connect('yaks.db')
cur = con.cursor()
con.text_factory = str
def job():
    cdict = {}
    cur.execute("""SELECT * FROM raw_yaks""")
    rows = cur.fetchall()
    for row in rows:
        cid = row[1]
        if cid not in cdict.keys():
            textToVotedic = {}
            textToVotedic[row[2].lower()] = row[3]
            cdict[cid] = [textToVotedic]
        else:
             textToVotedic = {}
             textToVotedic[row[2].lower()] = row[3]
             cdict[cid].append(textToVotedic)
    return cdict

def common_words_algorithm():
    allwords = {}
    collegedict = job()
    for college in collegedict.keys():
        for yak in college:
            for text, vote in yak: 
    cdict = common_dicts()
    word_dict = {}

def all_words(d):
        allw = {}
        for word in cdict.keys():
        allw = ' '.join(cdict[college])
        cword = common_word(all_words)
        word_dict[college] = cword
    return word_dict


print(job())



