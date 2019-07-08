from bs4 import BeautifulSoup
import requests


def get_soup(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    return soup

def pull_links(url, soup):
    newlist = []
    '''gives links to redirect to main subcategory screen'''
    #soup.find_all("a")
    anime_manga = soup.find("li", id = "medium_5")
    books = soup.find("li", id = "medium_3")
    cartoons = soup.find("li", id = "medium_4")
    celebs_real = soup.find("li", id = "medium_7")
    movies = soup.find("li", id = "medium_2")
    music = soup.find("li", id = "medium_6")
    others = soup.find("li", id = "medium_8")
    theater = soup.find("li", id = "medium_30198")
    tv_shows = soup.find("li", id = "medium_1")
    video_games = soup.find("li", id = "medium_476")
    uncategorized = soup.find("li", id = "medium_9971")

    #print(anime_manga.a.get("href"))
    newlist.append(str(anime_manga.a.get("href")))
    newlist.append(str(books.a.get("href")))
    newlist.append(str(cartoons.a.get("href")))
    newlist.append(str(celebs_real.a.get("href")))
    newlist.append(str(movies.a.get("href")))
    newlist.append(str(music.a.get("href")))
    newlist.append(str(others.a.get("href")))
    newlist.append(str(theater.a.get("href")))
    newlist.append(str(tv_shows.a.get("href")))
    newlist.append(str(video_games.a.get("href")))
    newlist.append(str(uncategorized.a.get("href")))
    
    return newlist


def list_categories(category: str) -> list:
    namelist = []
    
    url = 'https://archiveofourown.org' + category
        
    #print(url)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    final = soup.find_all("ul", class_="tags index group")
    for i in final:
        #print(i.find_all("li"))
        for j in i.find_all("li"):
            #print('start ---->' + str(j.text) + '<----here')
            #print(str(j.text).strip())
            final = (str(j.text).strip()).split()[-1]
            #print(final[1:-1])
            try:
                checker = int(final[1:-1])
                if checker > 200:
                    x = str(j.text.strip()).replace('\n', '')
                    truth = x.split()[:-1]
                    finalstr = ''
                    for i in truth:
                        finalstr += i+' '
                        #print(x)
                        #print(finalstr[:-1])
                    namelist.append(finalstr)
            except:
                continue
                

    return (namelist)
        
        
        
        
    

#print(newlist)
url = 'https://archiveofourown.org/'
first = get_soup(url)
bs = (pull_links(url, first))
#genre_list = ['/media/Anime%20*a*%20Manga/fandoms', '/media/Books%20*a*%20Literature/fandoms', '/media/Cartoons%20*a*%20Comics%20*a*%20Graphic%20Novels/fandoms',
#              '/media/Celebrities%20*a*%20Real%20People/fandoms', '/media/Movies/fandoms', '/media/Music%20*a*%20Bands/fandoms',
#              '/media/Other%20Media/fandoms', '/media/Theater/fandoms', '/media/TV%20Shows/fandoms',
#              '/media/Video%20Games/fandoms', '/media/Uncategorized%20Fandoms/fandoms']
print(list_categories(bs[10]))

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^ example of code. the bs used in final print statement is basically the same as the genre_list provided. 
