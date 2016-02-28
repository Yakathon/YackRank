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
		data.append({"name":row[3], "latitude":row[1], "longitude":row[2], "word":text[0]})
		counter += 1
	with open('static/data.json', 'w') as outfile:
		json.dump(data, outfile)
	print(data)
	#return data

#getJson()
