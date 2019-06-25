import urllib.request
from collections import defaultdict
from fanfiction import Scraper


def build_url_search():
    '''im hella lazy but when i do ill make a function that builds url based on search?? idk up to y'all. but every function here uses the URL given so I need to give each function a URL parameter, except the last function.'''
    pass


def retrieve_page_one():
    response = urllib.request.urlopen('https://www.fanfiction.net/anime/Alice-19th/') ### can make search query to generate url properly. will make function later to get different URLS. 
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
                    if metadata['num_words'] < 5000:
                        stories[storyid] = metadata
                        story = scraper.scrape_story(storyid)
                        #print(story)
    return stories
        
                
        
    
#^^^^^^^^ testing defaultdict shit. 





    



        
