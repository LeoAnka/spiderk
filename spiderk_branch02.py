


import sqlite3
import urllib.request
from bs4 import BeautifulSoup
import re
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


url = "http://www.faz.net/aktuell/wirtschaft/unternehmen/deutsche-bahn-auf-chef-suche-alles-hoert-auf-kein-kommando-14844033.html"

# check url is correct and exists
urlcode = urllib.request.urlopen(url).getcode()
print("urlcode", urlcode) # if code = 200, all is ok


web = urllib.request.urlopen(url).read()  #.decode('utf8') to see html tree

"""
print ("01 - TEXTO BRUTO EN BINARIO -----------------------------------------------------------")
print (web)
"""

htmlsoup = BeautifulSoup(web, "html.parser")
#print(soup) to see the html code from the website


"""
# Quita el texto que haya dentro de las etiquetas <script> (código javascript) y <style> (Estilos CSS).
# Ninguno de esos textos nos interesa.
for script in soup(["script", "style"]):
    script.extract()
"""

entries = htmlsoup.find_all("div")
#print(entries)
