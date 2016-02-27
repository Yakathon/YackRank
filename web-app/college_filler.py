import sqlite3

conn = sqlite3.connect('flaskr.db')
c = conn.cursor()

def insert(array, words):
	print(words)
	array.append((float(words[1]), float(words[2]), words[0]))

def setAll():
	school_pos = []
	with open('50schools.txt') as f:
		for line in f:
			words = [i.strip() for i in line.split(',')]
			insert(school_pos, words)
	c.executemany('INSERT INTO colleges (latitude, longitude, name) VALUES (?,?,?)', school_pos)
	conn.commit()
	conn.close()

setAll();
