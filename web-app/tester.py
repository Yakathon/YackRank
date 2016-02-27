# Import client classes from Yaklient
import csv, sqlite3
from yaklient import *

# Specify location of University of Exeter on a map
#location = Location(50.7365, -3.5344)
#user = User(exeter, "21C6CA60E3AA43C4B8C18B943394E111")




def databasemaker(location,college_id ):
    con = sqlite3.connect('/tmp/yaks.db')
    cur = con.cursor()
    user = User(location, "21C6CA60E3AA43C4B8C18B943394E111")

    
    i = college_id
   
    for yak in user.get_yaks():
        #cur.execute("INSERT INTO raw_yaks VALUES (?,?,?,?);",(i,college_id,yak.message,yak.score))
        #con.commit()
        print(yak)
        i = i + 1
    con.close() # closes connection to database


    # Get yaks, iterate through them, and print them

    #file.write(str(yak))
    #file.write("\n")

con = sqlite3.connect('flaskr.db')
cur = con.cursor()
cur.executescript("""
            DROP TABLE IF EXISTS raw_yaks;
            CREATE TABLE raw_yaks (yak_id INT, college_id INT, yak_text text,upvotes INT);""") # checks to see if table exists and makes a fresh table.
con.commit()
con.close() 
con = sqlite3.connect('flaskr.db')
cur = con.cursor()
cur.execute("""SELECT * FROM colleges""")
colleges = cur.fetchall()
for college in  colleges:
    college_id = college[0]
    lattitude = college[1]
    longitude = college[2]
    print(college[3])
    location = Location(lattitude,longitude)
    databasemaker(location,college_id)






