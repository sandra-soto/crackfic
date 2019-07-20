from bs4 import BeautifulSoup
import requests

def get_auth_data(url:str) -> dict:
    '''takes the url of the specific story<---- and returns dict of data'''
    url = "https://archiveofourown.org/" + url
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    final = soup.find("a", rel = "author")
    x = final.get("href")
    auth_name = str(final.text)
    another = soup.find("dd", class_ = "words")
    word_count = int(another.text)
    titlesearch = soup.find("h2", class_ = "title heading")
    title = str(titlesearch.text)

    newdict = {"Title": title, "Author": auth_name, "Words": word_count}

    return newdict

##print(get_auth_data('https://archiveofourown.org/works/17740550/chapters/41855435'))
    
    
