# Import client classes from Yaklient
from yaklient import *

# Specify location of University of Exeter on a map
exeter = Location(50.7365, -3.5344)

# Create user object at University of Exeter with given userid
user = User(exeter, "21C6CA60E3AA43C4B8C18B943394E111")

# Get yaks, iterate through them, and print them
for yak in user.get_yaks():
    print(yak)
