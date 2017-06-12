import sqlite3
import urllib.request
from bs4 import BeautifulSoup
import re
import sys
import time
#import ssl


# Deal with SSL certificate anomalies Python > 2.7
#scontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)


scontext = None


#[x] Elegir una página web.
#[x] Extraer el texto de esa página.
#[x] Limpiarlo de caracteres no válidos
#[x] Dividirlo en palabras.
#[x] Quitar las palabras no válidas (números, artículos, etc.).
#[x] Guardar cada palabra y el número de veces que ha salido.
#[x] clean web url end
#[] Interrupt crl + C by user


#------------------------

# cleaning of the text
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
#------------------------

# cleaning url
def cleanUrl(url):
    pos = len(url)
    if url[pos-1] == "/":     # check if url ends with "/" and removes it
        cleanedUrl = url[0:pos-1]
        return cleanedUrl
    else:
        return url

#------------------------




database = sqlite3.connect("dbwords.sqlite")
cur = database.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS words (word TEXT UNIQUE, count INTEGER)""")

cur.execute("""CREATE TABLE IF NOT EXISTS links (url TEXT UNIQUE)""")



#url = "http://www.faz.net/aktuell/wirtschaft/unternehmen/deutsche-bahn-auf-chef-suche-alles-hoert-auf-kein-kommando-14844033.html"
#url = "http://slowgerman.com/"
#url = "http://elpais.com/"

try:
    url = input("WEB LINK to analyse (or just ´ENTER´ for example web):")
    if len(url) < 1:
        url = "http://www.faz.net/aktuell/wirtschaft/unternehmen/deutsche-bahn-auf-chef-suche-alles-hoert-auf-kein-kommando-14844033.html"
        print("\nDefault web will be:")
        print("http://www.faz.net/aktuell/wirtschaft/unternehmen/deutsche-bahn-auf-chef-suche-alles-hoert-auf-kein-kommando-14844033.html")
    url = cleanUrl(url)

except:
    url = "http://www.faz.net/aktuell/wirtschaft/unternehmen/deutsche-bahn-auf-chef-suche-alles-hoert-auf-kein-kommando-14844033.html"
    print("wrong input. Default web will be:\n\n")
    print("http://www.faz.net/aktuell/wirtschaft/unternehmen/deutsche-bahn-auf-chef-suche-alles-hoert-auf-kein-kommando-14844033.html")

try:
    # check url is correct and exists
    urlcode = urllib.request.urlopen(url).getcode()
    if urlcode == 200:                        # if code = 200, all is ok
        print("\nconection success with your web:")
        print(url)
        print("\n")
except:
    print("could not open this web")


#check if web already scraped
cur.execute("SELECT url FROM links WHERE url = ?", (url,))
try:
    dbUrl = cur.fetchone()[0]
    print("This web was already analysed:\n%s" %dbUrl)
    analysed = True

except:
    print("Analysing selected web:\n%s" %url)
    analysed = False

if analysed == True:
    sys.exit(0)


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
        if len(word)<2: # to make sure it is a word and not just a letter
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



for foundword in dicSorted[0:250]:
    #print(foundword)

    #cur.execute("INSERT OR IGNORE INTO words (word, count) VALUES (?, ?)", (foundword, dic[foundword]))
    cur.execute("SELECT word FROM words WHERE word = ?", (foundword,))

    try:
        word = cur.fetchone()[0]
        cur.execute("UPDATE words SET count = count + ? WHERE word = ?", (dic[foundword], foundword))
    except:
        cur.execute("INSERT OR IGNORE INTO words (word, count) VALUES (?, ?)", (foundword, dic[foundword]))

#database.commit()

cur.execute("INSERT OR IGNORE INTO links (url) VALUES (?)", (url,))

database.commit()
