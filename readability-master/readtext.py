from readability import Readability

def readtext(string):
    read = Readability(string)
    print(read.FleschReadingEase())

readtext("Hi.")