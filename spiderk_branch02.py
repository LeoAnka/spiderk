import sqlite3
import urllib.request
from bs4 import BeautifulSoup
import re
#import ssl


# Deal with SSL certificate anomalies Python > 2.7
#scontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)


scontext = None


# Elegir una página web.
# Extraer el texto de esa página.
# Limpiarlo de caracteres no válidos
# Dividirlo en palabras.
# Quitar las palabras no válidas (números, artículos, etc.).
# Guardar cada palabra y el número de veces que ha salido.


#------------------------

# claning of the text
def textCleaner(text):
    text.strip()
    if len(text)<1:
        return text
    text = text.lower()
    chars = "0123456789/\"&.!$?,:;-_()„=´{}[]<>@%·|ºª"
    for c in chars:
        text = text.replace(c, " ")
    return text

#------------------------




conn = sqlite3.connect("webdata.sqlite")
cur = conn.cursor()


url = "http://www.faz.net/aktuell/wirtschaft/unternehmen/deutsche-bahn-auf-chef-suche-alles-hoert-auf-kein-kommando-14844033.html"
#url = "http://slowgerman.com/"
#url = "http://elpais.com/"

# check url is correct and exists
urlcode = urllib.request.urlopen(url).getcode()
if urlcode == 200:                        # if code = 200, all is ok
    print("\nconection success with your web:")
    print(url)
    print("\n")


web = urllib.request.urlopen(url).read()  #.decode('utf8') to see html tree

"""
print ("01 - TEXTO BRUTO EN BINARIO -----------------------------------------------------------")
print (web)
"""

htmlsoup = BeautifulSoup(web, "html.parser")
#print(soup) to see the html code from the website



# Quita el texto que haya dentro de las etiquetas <script> (código javascript) y <style> (Estilos CSS).
# Ninguno de esos textos nos interesa.
for script in htmlsoup(["script", "style"]):
    script.extract()


entries = htmlsoup.find_all("div")
#print(entries)

wordsList = []

for entry in entries:
    text = entry.getText()
    cleanedText = textCleaner(text) # clean text function
    #print(cleanedText)

    words = cleanedText.split()

    for word in words:
        if len(word)<2:
            continue
        else:
            wordsList.append(word)

"""
for word in wordsList:
    print(word)                     #TO SEE EXTRACTED WORDS
"""

dic = {}

for word in wordsList:
    dic[word] = dic.get(word, 0)
    dic[word] += 1

#print(dic)
#print(sorted(dic))                 #ORDER BY DIC KEYS
#print(sorted(dic, key=dic.get))   #ORDER BY DIC VALUES

dicSorted = sorted(dic, key=dic.get, reverse=True)
#print(dicSorted)                    #dicSorted is a LIST

"""
for word in dicSorted:
    print(word, dic[word])         #TO SEE SORTED DICTIONARY

for word in dicSorted[0:11]:       #TO SEE SORTED DICTIONARY enties 1-10
    print(word, dic[word])
"""

database = sqlite3.connect("dbwords.sqlite")
cur = database.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS words (word TEXT UNIQUE, count INTEGER)""")

cur.execute("""CREATE TABLE IF NOT EXISTS links (url TEXT UNIQUE)""")

for word in dicSorted[0:101]:
    #print(word)
    cur.execute("INSERT INTO words (word, count) VALUES (?, ?)", (word, dic[word]))
database.commit()
