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

filters = ["die", "der", "und", "von"]

#while (many > 0):

allwords = "SELECT word, count FROM words ORDER BY count DESC"
filterwords = []
filtered = False

for row in cur.execute(allwords):
    for word in filters:
        if row[0] == word:
            #print("word filtered")
            filtered = True
            break
        else:
            filtered = False
            continue

    if filtered == False:
        filterwords.append((row[0], row[1]))
        many -= 1
        #print("many left:", many)
        if (many < 1):
            break


for row in filterwords:
    print(row[0], row[1])
