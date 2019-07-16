from bs4 import BeautifulSoup
import requests

def get_auth_data(url:str) -> dict:
    '''takes the url of the specific story<---- and returns dict of data'''
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    final = soup.find("a", rel = "author")
    x = final.get("href")
    auth_url = "https://archiveofourown.org" + str(x)
    auth_name = str(final.text)
    another = soup.find("dd", class_ = "words")
    word_count = int(another.text)
    ##print(word_count)

    newdict = {"Author": auth_name, "Redirect": auth_url, "Words": word_count}

    return newdict

##get_auth_data('https://archiveofourown.org/works/17740550/chapters/41855435')
    
    
