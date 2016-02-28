#import enchant
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
    len_dict = {}
    for college in cdict.keys():
        all_words = ' '.join(cdict[college])
        number, yaks = spellcheck(all_words)
        word_dict[college] = number
        len_dict[college] = yaks
    return word_dict,len_dict
    
def spellcheck(all_words):
	s = set(nltk.corpus.stopwords.words('english'))
	#d = enchant.Dict("en_US")
	
	tokens = nltk.word_tokenize(all_words)
	count = 0
	#for word in tokens:
	    #if(d.check(word) == False):
	    	
	    	#count = 1 + count

	return count/len(tokens), len(tokens)

def populateNumYaksDB():
    con = sqlite3.connect('yaks.db')
    cur = con.cursor()
    con.text_factory = str
    cur.execute('DELETE FROM num_yaks')

    word_dict, num_dict = common_words_algorithm()
    for i in num_dict.items():
        print(i)
        cur.execute('INSERT INTO num_yaks (college_id, yaks) VALUES (?,?)', i)
    con.commit()
    con.close()







