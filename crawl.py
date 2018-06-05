#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests, re, json, string, random, sys, argparse, csv
from bs4 import BeautifulSoup
sys.setrecursionlimit(1500)

HTML_PARSER = "html.parser"
ROOT_URL = 'https://styleme.pixnet.net' 
# =====本日熱門=====
# TECH_URL = 'https://www.pixnet.net/blog/articles/category/24/hot/'        # 數位生活(14 pages)
# MAKEUP_URL = 'https://www.pixnet.net/blog/articles/category/23/hot/'        # 美容彩妝(25 pages)                
# MOVIE_URL = 'https://www.pixnet.net/blog/articles/category/19/hot/'        # 電影評論(6 pages)
# FOOD_URL = 'https://www.pixnet.net/blog/articles/group/3/hot/'        # 美味食記(94 pages)
# ENTERTAIN_URL = 'https://www.pixnet.net/blog/articles/category/31/hot/' #視聽娛樂(9 pages)
# FASHION_URL = 'https://www.pixnet.net/blog/articles/category/22/hot/' #時尚流行(16 pages)
# ARTCRITICS_URL = 'https://www.pixnet.net/blog/articles/category/17/hot/' #藝文評論(3 pages)
# CARS_URL = 'https://www.pixnet.net/blog/articles/category/42/hot/' #汽機車(4 pages)

# =====所有=====
# ENTERTAIN_URL = 'https://www.pixnet.net/blog/articles/group/1/hot/' #所有娛樂(23 pages)
# TRAVEL_URL = 'https://www.pixnet.net/blog/articles/group/2' #所有旅遊
# FOOD_URL = 'https://www.pixnet.net/blog/articles/group/3/hot/'    # 美味食記(94 pages)
# FASHION_URL = 'https://www.pixnet.net/blog/articles/group/4/hot' #所有流行
# THREEC_URL = 'https://www.pixnet.net/blog/articles/category/24/hot/' #所有3c

contents = []
article_count = 0

def arg_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', default='', type=str)
    parser.add_argument('--type', default='', type=str)
    # parser.add_argument('--num', type=int)
    args = parser.parse_args()
    return args


def get_item_link_list(type, url):
    global article_count
    global contents
    article_count = 0
    contents.clear()
    links = [] 
    for i in range(100):
        # if type == 'tech':
        #     list_url = TECH_URL
        # elif type == 'makeup':
        #     list_url = MAKEUP_URL            
        # elif type == 'movie':
        #     list_url = MOVIE_URL   
        # elif type == 'food':
        #     list_url = FOOD_URL
        # elif type == 'entertain':
        #     list_url = ENTERTAIN_URL
        # elif type == 'fashion':
        #     list_url = FASHION_URL
        # elif type == 'cars':
        #     list_url = CARS_URL
        # elif type == 'artcritics':
        #     list_url = ARTCRITICS_URL            
        list_url = url
        list_url = list_url + str(i+1)
        list_req = requests.get(list_url)
        print('URL :', list_url, '\n')
        print('Status : ', list_req, '\n')
        
        if list_req.status_code == requests.codes.ok:
            soup = BeautifulSoup(list_req.content, HTML_PARSER)
            if i == 0:
                articles = soup.find_all('div', attrs={'class' : 'featured'})
                articles.extend(soup.find('ol', attrs={'class' : 'article-list'}).find_all('li', attrs={'class' : re.compile("^rank")}))
            else:
                articles = soup.find('ol', attrs={'class' : 'article-list'}).find_all('li', attrs={'class' : re.compile("^rank")}) 
            for doc in articles:
                link = doc.find('a')['href']
                # link = link.split('post')[0]+'post'+link.split('post')[-1].split('-')[0]
                title = doc.find('h3').find('a', attrs={'target': '_blank'}).string

                print('title: ', title , '\n')
                print('link: ', link, '\n')
                # print('doc: ', doc ,'\n')

                if not any(i['title'] == title for i in links):
                    parse_item_information(title, link, 'article-content-inner',type)
                    links.append({
                        'title': title,
                        'href': link
                    })
                if article_count >= 1000:
                    return True



def parse_item_information(title, link, classname, type):
    req = requests.get(link)
    if req.status_code == requests.codes.ok:
        soup = BeautifulSoup(req.content, HTML_PARSER)
        content = soup.find('div', attrs={'class': classname})

        content = re.sub("<.*?>", " ", str(content))
        content = content.replace('\n',';')
        content = content.replace('\xa0','')
        content = content.replace('\r',';')
        content_html = ''
        word_count = 0
        article_viewcount = parse_article_viewcount(soup)
        global article_count
        for l_id, line in enumerate(content.split(';')):
            content_html+='<p>'
            for w_id, word in enumerate(line): 
                content_html+='<word id="'+str(l_id)+'-'+str(w_id)+'">'+word+'</word>'
                word_count += 1
            content_html+='</p>'

        # without word_count
        # if word_count >= 500 and word_count <= 3000:
        index = random.choice(string.ascii_letters)+link.rsplit('/', 1)[1]
        contents.append({'id':index, 'title':title, 'link':link, 'number': article_count, 'item_name':'', 'item_store':'',
        'status':'untagged', 'view_count': article_viewcount, 'word_count': word_count, 
        'content_s':content_html, 'content_w':content_html})
        # contents.append({'id':index, 'title':title, 'link':link, 'number': article_count, 'item_name':'', 'item_store':'' 
        # , 'content_s':content_html, 'content_w':content_html, 'word_count': word_count})        
        article_count += 1


def parse_article_viewcount(soup):
    try:
        source = soup.find('div', attrs={'class' : 'hslice box', 'id' : 'counter'}).find('script')
        counter_link = ''
        for _, i in enumerate(source):
            counter_link = 'http://'+str(i).split('//')[1].split("')")[0]
        
        counter_text = 0
        trial = 0
        while(counter_text == 0 and trial < 3):
            counter_response = requests.get(counter_link, auth=('user', 'pass'))
            counter_text = counter_response.text
            counter_text = int(counter_response.text.split('text(')[1].split(')')[0])
        return counter_text

    except:
        return 0
            


def crawler(type, url):
    get_item_link_list(type, url)
    print('complete, total', article_count, ' docs get!\n')
    with open('data/'+ type +'.json','w') as f: json.dump(contents, f)
    # if type == 'tech':
    #     with open('data/tech.json','w') as f: json.dump(contents, f)
    # elif type == 'makeup':
    #     with open('data/makeup.json','w') as f: json.dump(contents, f)      
    # elif type == 'movie':
    #     with open('data/movie.json','w') as f: json.dump(contents, f)
    # elif type == 'food':
    #     with open('data/food.json','w') as f: json.dump(contents, f)
    # elif type == 'entertain':
    #     with open('data/entertain.json','w') as f: json.dump(contents, f)
    # elif type == 'fashion':
    #     with open('data/fashion.json','w') as f: json.dump(contents, f)        
    # elif type == 'cars':
    #     with open('data/cars.json','w') as f: json.dump(contents, f)
    # elif type == 'artcritics':
    #     with open('data/artcritics.json','w') as f: json.dump(contents, f)
           

if __name__ == '__main__':
    args = arg_parse()
    crawler(args.type, args.url)
    ## type: tech; makeup; movie; food
    # crawler('tech')
    # crawler('entertain')
    # crawler('fashion')
    # crawler('cars')
    # crawler('artcritics')
    # crawler('makeup')
    # crawler('movie')
    # crawler('food')
