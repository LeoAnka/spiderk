

import sqlite3
import urllib.request
from bs4 import BeautifulSoup
#import ssl


# Deal with SSL certificate anomalies Python > 2.7
#scontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)


scontext = None


# 1. Elegir una página web.
# 2. Extraer el texto de esa página.
# 3. Dividirlo en palabras.
# 4. Quitar las palabras no válidas (números, artículos, etc.).
# 5. Guardar cada palabra y el número de veces que ha salido.


conn = sqlite3.connect("webdata.sqlite")
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

# Quita el texto que haya dentro de las etiquetas <script> (código javascript) y <style> (Estilos CSS).
# Ninguno de esos textos nos interesa.
for script in soup(["script", "style"]):
    script.extract()


dataText = soup.get_text()
text = dataText.strip()
print (text)





# Mejor solución: http://stackoverflow.com/questions/1936466/beautifulsoup-grab-visible-webpage-text

#tags = soup.find_all("p")
#for tag in tags:
    #print (soup.get_text())

# texts = soup.findAll(text=True)
# print(texts)
