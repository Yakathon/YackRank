# Import client classes from Yaklient
import csv, sqlite3
from yaklient import *

# Specify location of University of Exeter on a map
#location = Location(50.7365, -3.5344)
#user = User(exeter, "21C6CA60E3AA43C4B8C18B943394E111")




def databasemaker(location,college_id ):
    con = sqlite3.connect('yaks.db')
    cur = con.cursor()
    user = User(location, "21C6CA60E3AA43C4B8C18B943394E111")
    yaks = user.get_yaks()
    for yak in yaks:
        cur.execute("INSERT INTO raw_yaks VALUES (?,?,?);",(college_id,yak.message,yak.score))
        con.commit()
        print(yak)

    con.close() # closes connection to database

con = sqlite3.connect('yaks.db')
cur = con.cursor()
con.execute('DELETE FROM raw_yaks')
con.commit()
cur.execute("""SELECT * FROM colleges""")
colleges = cur.fetchall()
for college in  colleges:
    college_id = college[0]
    lattitude = college[1]
    longitude = college[2]
    print(college[3])
    location = Location(lattitude,longitude)
    print(location)
    databasemaker(location, college_id)






