##decodertest

import urllib.request


official_url = 'https://www.fanfiction.net/'

def main_category(category: str):
    '''use this func to generate the url for category that gives the different subcategories if applicable'''
    return official_url + category

def generate_subs(url: str):
    '''returns a list of subcategories'''
    response = urllib.request.urlopen(url)
    data = response.read()
    response.close()
    text = data.decode()
    x = text.split()
    categoryset = list()
    for i in x:
        if "href" in i and "/anime/" in i:
            if "</li>" not in i:
                clean = i[13:].index("/")
                categoryset.append(i[13:][:clean])

    return (categoryset)
        
