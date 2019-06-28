##decodertest
from bs4 import BeautifulSoup
import requests

import urllib.request


official_url = 'https://www.fanfiction.net/'

def main_category(category: str):
    '''use this func to generate the url for category that gives the different subcategories if applicable'''
    return official_url + category


def generate_subs(url: str):
    '''return list of subcategories. **UPDATED**'''
    #subcats = []
    page = requests.get(url)
    #text = page.content.decode(encoding = 'utf-8')
    #official = text.splitlines()
    #print(official)
    soup = BeautifulSoup(page.content, 'html.parser')
    subcats = soup.find_all("a")
    count = soup.find_all("span", class_ = "gray")
    countlist = []
    for i in count:
        x = str(i.contents[0])[1:-1]
        #print(x)
        #print(type(x))
        try:
            value = (int(x))
            #print(type(value))
            if value > 500:
                countlist.append(True)
            else:
                countlist.append(False)
        except:
            countlist.append(True)
    newfilter = []
    for i in subcats:
        title = i.get('title')
        newfilter.append(title)
    finalfilter = []
    for i in newfilter:
        if i != None:
            finalfilter.append(i)
    reallyfinal = []
    for i in finalfilter:
        if "\\'" in str(i):
            x = i.replace("\\", '')
            reallyfinal.append(x)
        else:
            reallyfinal.append(str(i))

    #print(countlist)
    actualfinallist = []      
    for i in range(len(countlist)):
        if countlist[i] == True:
            actualfinallist.append(reallyfinal[i])

    #print((actualfinallist))
    return (sorted(actualfinallist))

    
#print(generate_subs('https://www.fanfiction.net/anime'))

