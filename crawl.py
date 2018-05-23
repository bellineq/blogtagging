import requests, re, json, string, random
from bs4 import BeautifulSoup

HTML_PARSER = "html.parser"
ROOT_URL = 'https://styleme.pixnet.net' 
TECH_URL = 'https://www.pixnet.net/blog/articles/category/24/hot/'        # tech
MAKEUP_URL = 'https://www.pixnet.net/blog/articles/category/23/hot/'        # makeup                
MOVIE_URL = 'https://www.pixnet.net/blog/articles/category/19/hot/'        # movie
FOOD_URL = 'https://www.pixnet.net/blog/articles/group/3/hot/'        # food
ENTERTAIN_URL = 'https://www.pixnet.net/blog/articles/category/31/hot/'


contents = []
article_count = 0

def get_item_link_list(type):
    global article_count
    global contents
    article_count = 0
    contents.clear()
    links = [] 
    for i in range(10):
        if type == 'tech':
            list_url = TECH_URL
        elif type == 'makeup':
            list_url = MAKEUP_URL            
        elif type == 'movie':
            list_url = MOVIE_URL   
        elif type == 'food':
            list_url = FOOD_URL
        elif type == 'entertain':
            list_url = ENTERTAIN_URL

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
                link = link.split('post')[0]+'post'+link.split('post')[-1].split('-')[0]
                title = doc.find('h3').find('a', attrs={'target': '_blank'}).string

                print('title: ', title , '\n')
                print('link: ', link, '\n')
                # print('doc: ', doc ,'\n')

                if not any(i['title'] == title for i in links):
                    parse_item_information(title, link, 'article-content-inner')
                    links.append({
                        'title': title,
                        'href': link
                    })
                if article_count >= 100:
                    return True



def parse_item_information(title, link, classname):
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
        global article_count
        for l_id, line in enumerate(content.split(';')):
            content_html+='<p>'
            for w_id, word in enumerate(line): 
                content_html+='<word id="'+str(l_id)+'-'+str(w_id)+'">'+word+'</word>'
                word_count += 1
            content_html+='</p>'
        if word_count >= 500 and word_count <= 3000:
            index = random.choice(string.ascii_letters)+link.rsplit('/', 1)[1]
            contents.append({'id':index, 'title':title, 'link':link, 'number': article_count, 'item_name':'', 'item_store':'', 
            'content_s':content_html, 'content_w':content_html})
            article_count += 1

def crawler(type):
    get_item_link_list(type)
    print('complete, total', article_count, ' docs get!\n')
    if type == 'tech':
        with open('data/tech.json','w') as f: json.dump(contents, f)
    elif type == 'makeup':
        with open('data/makeup.json','w') as f: json.dump(contents, f)      
    elif type == 'movie':
        with open('data/movie.json','w') as f: json.dump(contents, f)
    elif type == 'food':
        with open('data/food.json','w') as f: json.dump(contents, f)
    elif type == 'entertain':
        with open('data/entertain.json','w') as f: json.dump(contents, f)        
    

if __name__ == '__main__':
    ## type: tech; makeup; movie; food
    # crawler('tech')
    crawler('entertain')
    # crawler('makeup')
    # crawler('movie')
    # crawler('food')