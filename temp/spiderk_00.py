

import sqlite3
import urllib.request
from bs4 import BeautifulSoup
#import ssl


# Deal with SSL certificate anomalies Python > 2.7
#scontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)


scontext = None




conn = sqlite3.connect("webdata")
cur = conn.cursor()


cur.execute(""" CREATE TABLE IF NOT EXISTS webs
    (ID INTEGER PRIMARY KEY, url TEXT UNIQUE, content TEXT) """)

#url = input("Enter url to feed webdata (or just ENTER to exit): ")
##if len(url)<1: exit()
#if len(url)<1: url = "https://www.deutschland.de/de/topic/politik/deutschland-europa/jahresvorschau-2017"
url = "http://www.faz.net/aktuell/wirtschaft/unternehmen/deutsche-bahn-auf-chef-suche-alles-hoert-auf-kein-kommando-14844033.html"

print ("web target is", url)


pass # check url is correct and exists

web = urllib.request.urlopen(url).read()
print (web)

soup = BeautifulSoup(web, "html.parser")



dataText = soup.get_text()
text = dataText.strip()
print (text)







#tags = soup.find_all("p")
#for tag in tags:
    #print (soup.get_text())
