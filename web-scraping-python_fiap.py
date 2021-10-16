import urllib.request
import re
from bs4 import BeautifulSoup

def getPage(link):
    page = urllib.request.urlopen(link)
    soup = BeautifulSoup(page,'html5lib')
    return soup

def getLinks(soup):
    lista = soup.find_all('a')
    return lista

def salvar(texto):
    arq = open("MBAs", "a")
    arq.write(texto)

links = getLinks(getPage("https://www.fiap.com.br/mba/"))
lista_links = []
for link in links: 
    result = re.search(r'https:\//www.fiap.com.br\/((^|)(mba|online))\/mba-\S+', str(link.get('href')))
    if result is None:
        continue
    lista_links.append( result.group(0) )

print("Localizados", len(lista_links), "links")

texto = ""
count = 0
for l in lista_links:
    soup = getPage(l)
    content = soup.find_all('p')
    count += 1
    print("[ "+str(count)+"/"+ str(len(lista_links))+" ]capturando texto do link -> " + l)
    new_str = str(l)  
    for cont in content:
        c = cont.get("class")
        if c is None:
            continue
        elif str(c[0]) == 'mba-curso-tema-alternativo-informacoes-item-text' or str(c[0]) == 'mba-curso-tema-alternativo-informacoes-item-text-special':
            texto = cont.text
    new_str += texto
    salvar(new_str)