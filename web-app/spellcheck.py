import enchant
import sqlite3
import nltk
import itertools
import operator

con = sqlite3.connect('yaks.db')
cur = con.cursor()

def common_dicts():
    cdict = {}
    cur.execute("""SELECT * FROM raw_yaks""")
    rows = cur.fetchall()
    for row in rows:
        cid = row[1]
        if cid not in cdict.keys():
            cdict[cid] = [row[2].lower()]
        else:
            cdict[cid].append(row[2].lower())
    return cdict


def common_words_algorithm():
    cdict = common_dicts()
    word_dict = {}
    for college in cdict.keys():
        all_words = ' '.join(cdict[college])
        number = spellcheck(all_words)
        word_dict[college] = number
    return word_dict
    
def spellcheck(all_words):
	s = set(nltk.corpus.stopwords.words('english'))
	d = enchant.Dict("en_US")
	
	tokens = nltk.word_tokenize(all_words)
	count = 0
	for word in tokens:
	    if(d.check(word) == False):
	    	
	    	count = 1 + count

	return count/len(tokens)

print(common_words_algorithm())






