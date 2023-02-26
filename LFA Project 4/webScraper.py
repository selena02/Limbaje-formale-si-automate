import requests
import re
from bs4 import BeautifulSoup
import json

def checkFilter(filter, title, description):
    t = re.search(rf"{filter}", title, flags=re.IGNORECASE)
    d = re.search(rf"{filter}", description, flags=re.IGNORECASE)
    if t or d:
        return True
    return False

def writeToJSONFile(path, fileName, data):
    filePathNameWExt = './' + path + '/' + fileName + '.json'
    with open(filePathNameWExt, 'w') as fp:
        json.dump(data, fp, sort_keys=True, indent=4, separators=(',', ': '))

filtersList = ("bicicleta", "geanta", "monede", "carte", "album", "disc", "pistol", "role", "trotineta", "tablou")
filtersDict = {0:[], 1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[], 8:[], 9:[]}


for page in range(1, 26):
    data = requests.get(f"https://www.olx.ro/hobby-sport-turism/?page={page}")
    soup = BeautifulSoup(data.text, 'html.parser')

    offersTable = soup.find('table', {'id': 'offers_table'})
    tbody = offersTable.find('tbody')

    for tr in tbody.find_all('tr', {'class':'wrap'}):
        link = tr.find('a')['href']
        dataOffer = requests.get(link)
        soupOffer = BeautifulSoup(dataOffer.text, 'html.parser')

        try:
            title = soupOffer.find('h1').text.strip()
        except:
            title = "N/A"

        try:
            description = soupOffer.find('div', {'class': 'css-g5mtbi-Text'}).text
        except:
            description = "N/A"

        try:
            image = soupOffer.find('img', {'class': 'css-1bmvjcs'})['src']
        except:
            image = "N/A"
        
        try:
            price = soupOffer.find('h3', {'class': 'css-okktvh-Text eu5v0x0'}).text.strip()
        except:
            price = "N/A"

        for i in range(10):
            if checkFilter(filtersList[i], title, description):
                filtersDict[i].append({"title": title, "link": link, "image": image, "price": price})

for i in range(0, 10):
    filtersDict[filtersList[i]] = filtersDict.pop(i) 

writeToJSONFile('./', 'result', filtersDict)
print("done")