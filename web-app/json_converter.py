import sqlite3
import json

conn = sqlite3.connect('yaks.db')
c = conn.cursor()

def getJson():
	data = []
	counter = 0
	c.execute('SELECT * FROM colleges ORDER BY college_id')
	for row in c.fetchall():
		c.execute('SELECT word_text FROM most_valuable_words WHERE college_id = ' + str(row[0]))
		text = c.fetchall()
		c.execute('SELECT yak_text FROM top_yaks WHERE college_id = ' + str(row[0]))
		top_yaks = c.fetchall()
		c.execute('SELECT yaks FROM num_yaks WHERE college_id = ' + str(row[0]))
		num_yaks = c.fetchall()
		c.execute('SELECT average_grade_level FROM college_grade_level WHERE college_id = ' + str(row[0]))
		college_grade_level = c.fetchall()
		c.execute('SELECT average_readability FROM college_readability WHERE college_id = ' + str(row[0]))
		college_readability = c.fetchall()
		c.execute('SELECT times_swore FROM times_swore WHERE college_id = ' + str(row[0]))
		times_swore = c.fetchall()

		data.append({"name":row[3], "latitude":row[1], "longitude":row[2], "word":text[0], "top_yaks":top_yaks[0], "num_yaks":num_yaks[0], "college_grade_level":college_grade_level[0], "college_readability":college_readability[0], "times_swore":times_swore[0]})
		counter += 1
	with open('static/data.json', 'w') as outfile:
		json.dump(data, outfile)
	print(data)
	#return data

#getJson()
