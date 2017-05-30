import sqlite3
import re


database = sqlite3.connect("dbwords.sqlite")
cur = database.cursor()

#many = 50           # User defines how many words wants to be displayed
try:
    many = int(input("how many words you want to see: "))
except:
    many = 50
    print ("wrong input. Default 50 words will be shown:\n")

for row in cur.execute("""SELECT word, count FROM words ORDER BY count DESC LIMIT ?""", (many,)):
    print(row[0], row[1])
