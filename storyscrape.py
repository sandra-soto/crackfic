import urllib.request
import urllib
#from collections import defaultdict
#from fanfiction import Scraper
from bs4 import BeautifulSoup
from random import randint
import requests


def get_story_text(url: str) -> str:
    '''pulls text from given url. example of url = https://archiveofourown.org/works/490307'''
    url = 'https://archiveofourown.org' + url
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    final = soup.find("div", class_ = "userstuff")
    storytext = ""
    for i in final:
        try:
            storytext += str(i.text) + "\n"
        except:
            continue
    return storytext
def test_function(url):
    response = urllib.request.urlopen(url)
    data = response.read()
    response.close()
    return str(data)

def correct_subcategory_link(subcategory:str): #returns the correct link for subcategory minus japanese titles for some reason
##    sbc = subcategory[:-1]
##    sbc = sbc.replace(" ", "%20")
##    sbc = sbc.replace("|", "%7C")
##    sbc = sbc.replace("&", "*a*")
##    sbc = sbc.replace(".", "*d*")
    sbc = urllib.parse.quote(subcategory)
    return sbc

def random_story_in_page(subcategory:str)-> str:
    subcat = correct_subcategory_link(subcategory)
    print(subcat)
    story_ids = generate_url(retrieve_story(subcat), subcat)
    print(story_ids)
    return get_story_text(story_ids[randint(0, len(story_ids) - 1)])
##    ranstory = correct_subcategory_link(subcategory)
##    return test_function(ranstory) #replaced the youtube thing with an archive link
    #returns a random story from a page, given category and subcategory
    #return test_function('https://www.youtube.com/')
    #return str(generate_random_page(category, subcategory)) timeout on link genreation
    #return get_story(generate_random_page(category, subcategory)[randint(0,24)])


def retrieve_story(subcat:str)-> str:
    '''take url from subcategory then get max num of pages. example of url parameter = https://archiveofourown.org/tags/07-Ghost/works'''
    url = 'https://archiveofourown.org/tags/' + subcat + '/works'
    print(url)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    final = soup.find("ol", class_ = 'pagination actions')
    print(final)
    #print(final.find_all("li")[-2].text)
    return int(final.find_all("li")[-2].text)

#print(retrieve_story('https://archiveofourown.org/tags/07-Ghost/works'))
#https://archiveofourown.org/works?utf8=%E2%9C%93&work_search%5Bsort_column%5D=revised_at&work_search%5Bother_tag_names%5D=&work_search%5Bexcluded_tag_names%5D=&work_search%5Bcrossover%5D=&work_search%5Bcomplete%5D=&work_search%5Bwords_from%5D=100&work_search%5Bwords_to%5D=1000&work_search%5Bdate_from%5D=&work_search%5Bdate_to%5D=&work_search%5Bquery%5D=&work_search%5Blanguage_id%5D=1&commit=Sort+and+Filter&tag_id=
####### ^^^^^^use this link to parse shit, add subcategory to end of this (make sure to urlify the subcategory in order for this to work) ####### 
####### ^^^^^^link should be used for retrieve_story function to get max pages, but shouldnt be used when the random int generated for page is > 1. that uses another kind of url. ########
####### if randint generates 1, then use this url template above ########

####### https://archiveofourown.org/tags/Boruto:%20Naruto%20Next%20Generations/works?commit=Sort+and+Filter&page=3&utf8=%E2%9C%93&work_search%5Bcomplete%5D=&work_search%5Bcrossover%5D=&work_search%5Bdate_from%5D=&work_search%5Bdate_to%5D=&work_search%5Bexcluded_tag_names%5D=&work_search%5Blanguage_id%5D=1&work_search%5Bother_tag_names%5D=&work_search%5Bquery%5D=&work_search%5Bsort_column%5D=revised_at&work_search%5Bwords_from%5D=100&work_search%5Bwords_to%5D=1000 #######
#######                                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^                              ^^^^^^
####### pointed toward areas that needed to be changed for the url 



def generate_url(num_pages: int, subcat: str):
    '''takes max pages and subcategory (must be urlified) and  generates stories on that page. example of subcat = Boruto:%20Naruto%20Next%20Generations'''

    page_num = randint(1, num_pages)
    print(page_num)
    
    url = "https://archiveofourown.org/tags/" + str(subcat) + "/works?commit=Sort+and+Filter&page=" + str(page_num) + "&utf8=%E2%9C%93&work_search%5Bcomplete%5D=&work_search%5Bcrossover%5D=&work_search%5Bdate_from%5D=&work_search%5Bdate_to%5D=&work_search%5Bexcluded_tag_names%5D=&work_search%5Blanguage_id%5D=1&work_search%5Bother_tag_names%5D=&work_search%5Bquery%5D=&work_search%5Bsort_column%5D=revised_at&work_search%5Bwords_from%5D=100&work_search%5Bwords_to%5D=1000"
    #url_sub += str(page_num)
    print(url)
    #url = "https://archiveofourown.org/works?utf8=%E2%9C%93&work_search%5Bsort_column%5D=revised_at&work_search%5Bother_tag_names%5D=&work_search%5Bexcluded_tag_names%5D=&work_search%5Bcrossover%5D=&work_search%5Bcomplete%5D=&work_search%5Bwords_from%5D=100&work_search%5Bwords_to%5D=1000&work_search%5Bdate_from%5D=&work_search%5Bdate_to%5D=&work_search%5Bquery%5D=&work_search%5Blanguage_id%5D=1&commit=Sort+and+Filter&tag_id=" + str(subcat)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    final = soup.find_all("h4", class_ = "heading")
    linklist = []
    for i in final:
        try:
            #print(i.a.get("href"))
            linklist.append(i.a.get("href"))
        except:
            continue
    ##### below code commented out because I didnt notice ao3 had filtering for language and wordcount. try now should be much faster #####
    #word_count = soup.find_all("dd", class_ = "words")
    #word_count_list = []
    #for i in word_count:
    #    word_count_list.append(int(str(i.text).replace(",", '')))

    #print(word_count_list)

    #languages = []
    #language = soup.find_all("dd", class_ = "language")
    #for i in language[:-1]:
    #    languages.append(str(i.text))

    #print(linklist)
    #print(languages)
    #print(word_count_list)
    #final_list = []
    #for i in range(len(linklist)):
    #    if languages[i] == "English" and word_count_list[i] <= 1000:
    #        #print('f')
    #        final_list.append(linklist[i])
        
        
    #print(final_list)
    return linklist
    #print(final)

#x = (generate_url(6, 'Boruto:%20Naruto%20Next%20Generations'))
#print(x)
#print(random_story_in_page('Cardfight!! Vanguard'))
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^(notes for generate_url function)
####a = generate_url(retrieve_story('https://archiveofourown.org/tags/07-Ghost/works'), 'https://archiveofourown.org/tags/07-Ghost/works')
####print(a)
#### returns ends of link: /works/429558
#### needs to be used like: https://archiveofourown.org/works/490307 ### will get url from here. 
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^




####print(get_story_text('https://archiveofourown.org/works/490307'))
    
