import requests, re, json, string, random
from bs4 import BeautifulSoup

HTML_PARSER = "html.parser"
ROOT_URL = 'https://styleme.pixnet.net' 
TECH_URL = 'https://www.pixnet.net/blog/articles/category/24/hot/'        # tech
MAKEUP_URL = 'https://www.pixnet.net/blog/articles/category/23/hot/'        # makeup                
MOVIE_URL = 'https://www.pixnet.net/blog/articles/category/19/hot/'        # movie
FOOD_URL = 'https://www.pixnet.net/blog/articles/group/3/hot/'        # food

# LIST_URL = 'https://www.pixnet.net/blog/articles/category/24/hot/'        # tech
# LIST_URL = 'https://www.pixnet.net/blog/articles/category/23/hot/'        # makeup                
# LIST_URL = 'https://www.pixnet.net/blog/articles/category/19/hot/'        # movie
# LIST_URL = 'https://www.pixnet.net/blog/articles/group/3/hot/'        # food

contents = [] 

def get_item_link_list(type):
    for i in range(5):
        if type == 'tech':
            list_url = TECH_URL
        elif type == 'makeup':
            list_url = MAKEUP_URL            
        elif type == 'movie':
            list_url = MOVIE_URL   
        elif type == 'food':
            list_url = FOOD_URL

        list_url = list_url + str(i+1)
        print('URL :', list_url, '\n')
        list_req = requests.get(list_url)
        print('Status : ', list_req, '\n')
        if list_req.status_code == requests.codes.ok:
            soup = BeautifulSoup(list_req.content, HTML_PARSER)
            if i == 0:
                articles = soup.find_all('div', attrs={'class' : 'featured'})
                articles.extend(soup.find('ol', attrs={'class' : 'article-list'}).find_all('li', attrs={'class' : re.compile("^rank")}))
            else:
                articles = soup.find('ol', attrs={'class' : 'article-list'}).find_all('li', attrs={'class' : re.compile("^rank")}) 

            links = []
            for doc in articles:
                # print('doc: ', doc ,'\n')
                link = doc.find('a')['href']
                link = link.split('post')[0]+'post'+link.split('post')[-1].split('-')[0]
                print('link: ', link, '\n')
                title = doc.find('h3').find('a', attrs={'target': '_blank'}).string
                print('title: ', title , '\n')
                links.append({
                    'title': title,
                    'href': link
                })
                parse_item_information(title, link, 'article-content-inner')


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
        for l_id, line in enumerate(content.split(';')):
            content_html+='<p>'
            for w_id, word in enumerate(line): content_html+='<word id="'+str(l_id)+'-'+str(w_id)+'">'+word+'</word>'
            content_html+='</p>'
        index = random.choice(string.ascii_letters)+link.rsplit('/', 1)[1]
        contents.append({'id':index, 'title':title, 'link':link, 'content': content_html})

def Binder(type):
    get_item_link_list(type)
    if type == 'tech':
        with open('data/tech.json','w') as f: json.dump(contents, f)
        with open('data/tech_w.json','w') as f: json.dump(contents, f)
        with open('data/tech_s.json','w') as f: json.dump(contents, f)
    elif type == 'makeup':
        with open('data/makeup.json','w') as f: json.dump(contents, f)
        with open('data/makeup_w.json','w') as f: json.dump(contents, f)
        with open('data/makeup_s.json','w') as f: json.dump(contents, f)        
    elif type == 'movie':
        with open('data/movie.json','w') as f: json.dump(contents, f)
        with open('data/movie_w.json','w') as f: json.dump(contents, f)
        with open('data/movie_s.json','w') as f: json.dump(contents, f) 
    elif type == 'food':
        with open('data/food.json','w') as f: json.dump(contents, f)
        with open('data/food_w.json','w') as f: json.dump(contents, f)
        with open('data/food_s.json','w') as f: json.dump(contents, f)
    

if __name__ == '__main__':
    ## type: tech; makeup; movie; food
    Binder('food')

    # get_item_link_list('movie')
    # with open('data/tech.json','w') as f: json.dump(contents, f)
    # with open('data/makeup.json','w') as f: json.dump(contents, f)
    # with open('data/movie.json','w') as f: json.dump(contents, f)
    # with open('data/food.json','w') as f: json.dump(contents, f)
