#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests, re, json, string, random, sys, argparse, csv
from bs4 import BeautifulSoup
sys.setrecursionlimit(1500)
maxInt = sys.maxsize
decrement = True

HTML_PARSER = "html.parser"


contents = []
article_count = 0


def get_item_link_list(category):
    """
        collect article links for articles list in the url,
        nPage: number of pages to crawl 
    """
    filepath = 'newLinks/'+category + '.csv'
    with open(filepath, 'r') as csvfile:
        global decrement
        global maxInt 
        while decrement:
        # decrease the maxInt value by factor 10 
        # as long as the OverflowError occurs.

            decrement = False
            try:
                csv.field_size_limit(maxInt)
            except OverflowError:
                maxInt = int(maxInt/10)
                decrement = True

        reader = csv.reader(csvfile)
        next(reader)
        data = []
        for row in reader:
            data.append([row[0],row[1]])
    csvfile.close()

    global article_count
    global contents
    article_count = 0
    contents.clear()

    for link, title in data:
        parse_item_information(title, link, 'article-content-inner')



def parse_item_information(title, link, classname):
    '''
        parse article content
    '''
    req = requests.get(link)
    if req.status_code == requests.codes.ok:
        soup = BeautifulSoup(req.content, HTML_PARSER)
        article_viewcount = parse_article_viewcount(soup)
        [s.extract() for s in soup('script')]
        content = soup.find('div', attrs={'class': classname})

        content = re.sub("<.*?>", " ", str(content))
        content = content.replace('\n',';')
        content = content.replace('\xa0','')
        content = content.replace('\r',';')
        content_html = ''
        word_count = 0
        global article_count
        for l_id, line in enumerate(content.split(';')):
            content_html+='<p>'
            for w_id, word in enumerate(line): 
                content_html+='<word id="'+str(l_id)+'-'+str(w_id)+'">'+word+'</word>'
                word_count += 1
            content_html+='</p>'

        
        ## define article index
        index = random.choice(string.ascii_letters)+link.rsplit('/', 1)[1].split('-')[0]
        
        results = {'id':index, 'title':title, 'link':link, 'number': article_count, 'item_name':'', 'item_store':'',
        'status':'untagged', 'view_count': article_viewcount, 'word_count': word_count, 
        'content_s':content_html, 'content_w':content_html}

        contents.append(results)       
        article_count += 1


def parse_article_viewcount(soup):
    '''
        parse viewcount
    '''
    try:
        source = soup.find('div', attrs={'class' : 'hslice box', 'id' : 'counter'}).find('script')      
        counter_link = ''
        for _, i in enumerate(source):
            counter_link = 'http://'+str(i).split('//')[1].split("')")[0]
        
        counter_text = 0
        trial = 0
        ## Try five times to collect view_count
        while(counter_text == 0 and trial < 5):
            counter_response = requests.get(counter_link, auth=('user', 'pass'))
            counter_text = counter_response.text
            counter_text = int(counter_response.text.split('text(')[1].split(')')[0])
        return counter_text

    except:
        print('exception')
        return 0
            


def crawler(category):
    get_item_link_list(category)
    print('complete, total', article_count, ' docs get!\n')
    with open('parsedData/'+ category+'.json','w') as f: 
        json.dump(contents, f)

           

if __name__ == '__main__':
    crawler('movie')
    crawler('tech')
    crawler('beauty')
