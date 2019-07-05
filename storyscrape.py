import urllib.request
from collections import defaultdict
#from fanfiction import Scraper
from bs4 import BeautifulSoup
from random import randint
import requests

def pull_links(url):
    #just part of the bigger function, nothing to see here. 
    '''this code is to be used in a for loop to get the link for each story present on a page. '''

    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    sublinks = soup.find_all("a", class_ = 'stitle')
    newlinks = []
    for i in sublinks:
        newlinks.append(str(i.get('href')))
    return newlinks


def get_pages(url):
    #works when given the subcategory, like https://www.fanfiction.net/Anime/Naruto/' needs subcategory = Naruto like in this example.
    #used in lower function, no need to worry about this. 
    '''gives me the number of pages i need to go through to get stories ON A SPECIFIC PAGE. THE URL MUST HAVE THE NEW PAGE ADDED TO IT IF NECESSARY.'''
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    searchmax = soup.find_all('a')
    for i in searchmax:
        if str(i.text) == "Last":
            x = int((str(i).index(";p=")))
            finalindex = x + 3
            #print(str(i)[finalindex:])
            endindex = str(i)[finalindex:].index('"')
            #print(str(i)[finalindex:][:endindex])
            return int(str(i)[finalindex:][:endindex])

#print(pull_links('https://www.fanfiction.net/anime/Alice-19th/'))
#print(get_pages('https://www.fanfiction.net/anime/Naruto/'))

def get_story_data(storyurl: str)->list:
    #used to display where story is from and details regarding the story. 
    '''gets author data of whomever wrote this particular story'''
    page = requests.get(storyurl)
    soup = BeautifulSoup(page.content, 'html.parser')
    searchdata = soup.find_all('span', class_='xgray xcontrast_txt')
    return (str(searchdata[0].text).split("-"))


def get_story(storyurl):
    #gets actual story text
    '''takes the url of the story and gets the story written by whomever did so.'''
    storyurl = 'https://www.fanfiction.net/' + storyurl
    page = requests.get(storyurl)
    soup = BeautifulSoup(page.content, 'html.parser')
    searchmax = soup.find_all('div', id = 'storytextp')
    for i in searchmax:
        return (str(i.text))


def generate_random_page(category: str,subcategory: str)-> list:
    #takes a random page from the subcategory and pulls a list of stories from that page. list length is 25
    #there is the case that the story does not have more less 1k words on the page... needs to be resolved. 
    '''takes the main and sub category to generate a random page in which will return a list of stories for that page only.'''
    nsubcategory = subcategory.replace(' ', '-') #####done so it should work in generating the results.
    ncategory = category.lower() ####works right with url
    url = 'https://www.fanfiction.net/' + category + '/' + nsubcategory
    #print(nsubcategory)
    num_pages = get_pages(url)
    select_page = randint(1, num_pages + 1)
    #print(select_page)
    if select_page > 1:
        url = 'https://www.fanfiction.net/' + category + '/' + nsubcategory + '/' + '?&srt=1&r=103&p=' + str(select_page)
        #print(url)
        return pull_links(url)
    else:
        return pull_links(url)

def random_story_in_page(category:str, subcategory:str)-> str:
    '''returns a random story from a page, given category and subcategory'''
    return get_story(generate_random_page(category, subcategory)[randint(0,24)])

##print(len(generate_random_page('anime', 'Inuyasha')))
##print(get_story(generate_random_page('anime','Naruto')[24]))

#print(random_story_in_page('anime', 'Naruto'))
    
    


'''
########################below this line is old code, don't think we need for the project. 
def retrieve_page_one(url):
    response = urllib.request.urlopen(url) ### can make search query to generate url properly. will make function later to get different URLS. 
    data = response.read()
    response.close()
    x = data.split()
    newlist = [] #can change to dicts to make this shit hella quick
    copylist = []
    count = 0
    for i in x:## simple way to get the different story links. 
        if "href" not in str(i):
            newlist.append(count)
        count += 1
    
    #print(newlist)
    # \/ this bs code adds for first page only. 
    for i in range(len(x)):
        if i not in newlist:
            if "/s/" in str(x[i]) or ("Last" in str(x[i]) and "srt" in str(x[i])): ## this or should only be used for page 1 of stories, after that it shouldnt check for LAST page #.    
                copylist.append(x[i])
    #print(str(copylist[0]))
    return copylist





def retrieve_all_links(copylist):
    newurl = 'https://www.fanfiction.net/anime/Alice-19th/?&srt=1&r=103&p='#end portion should be universal for all categories. this should be updated.
    x = str(copylist[0][int(str(copylist[0]).index("&p")):])
    y = str(copylist[0][int(str(copylist[0]).index("&p")):]).index("'")
    x = x[3:y] #<----------- gives me proper number of pages to go through to get different stories.
    print(newurl + x)
    data = urllib.request.urlopen(newurl + x)
    final = data.read()

    ###### This code block meant to go through the remaining pages to get all the different stories available.

    for i in range(2, int(x) + 1):
        data = urllib.request.urlopen(newurl + str(i))
        final = data.read()
        text = final.split()
        newlist = []
        for i in text:
            if "href" not in str(i):
                newlist.append(count)
            count += 1

        for i in range(len(text)):
            if i not in newlist:
                if "/s/" in str(text[i]):
                    copylist.append(text[i])
    return copylist
    ###### Finished getting remaining stories.



#///////////////////////# parse through list of links to get the story IDS.
def story_retrieve(copylist):
    
    stories = defaultdict(dict)

    for i in copylist:
        
        #print(i)
        cutpart1 = str(i)[11:]
        indexid = cutpart1.index("/")
        finalcut = cutpart1[:indexid]
        try:
            storyid = int(finalcut)
            
        except:
            continue
        else:
            try:
                scraper = Scraper()
                metadata = scraper.scrape_story_metadata(storyid)
                #print(metadata)
            except:
                print('EXTREME ERROR OCCURRED HERE <------------------"')
                continue
                    #print(metadata)
            else:
                
                if storyid not in stories:
                    if metadata['num_words'] < 1000:
                        stories[storyid] = metadata
                        story = scraper.scrape_story(storyid)
                        #print(story)
    return stories
        
                
        
    
#^^^^^^^^ testing defaultdict shit. 
'''




    



        
