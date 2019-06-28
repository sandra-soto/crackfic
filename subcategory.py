##decodertest
from bs4 import BeautifulSoup
import requests

import urllib.request


official_url = 'https://www.fanfiction.net/'

def main_category(category: str):
    '''use this func to generate the url for category that gives the different subcategories if applicable'''
    return official_url + category


def generate_subs(url: str, category: str):
    '''return list of subcategories. **UPDATED**'''
    #subcats = []
    page = requests.get(url)
    #text = page.content.decode(encoding = 'utf-8')
    #official = text.splitlines()
    #print(official)
    soup = BeautifulSoup(page.content, 'html.parser')
    subcats = soup.find_all("a")
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
            
    
    print(reallyfinal)
        

