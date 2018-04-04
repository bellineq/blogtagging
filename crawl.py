import requests, re, json
from bs4 import BeautifulSoup

HTML_PARSER = "html.parser"
ROOT_URL = 'https://styleme.pixnet.net'                 # TODO!
LIST_URL = 'https://styleme.pixnet.net/makeupsharing'   # TODO!
# ROOT_URL = 'https://tech3c.pixnet.net/category/24'

contents = []  # 儲存取得的文章資料

def get_item_link_list():
    list_req = requests.get(LIST_URL)
    if list_req.status_code == requests.codes.ok:
        soup = BeautifulSoup(list_req.content, HTML_PARSER)
        articles = soup.find_all('div', attrs={'class': 'article-bg'})  # TODO!
        # articles = soup.find_all('div', attrs={'class': 'gird-item__body'})

        links = []
        for a in articles:
            link = ROOT_URL+a.find('a')['href']
            title = a.find('a', attrs={'class': 'article__content__title--single'}).string  # TODO!
            links.append({
                'title': title,
                'href': link
            })
            parse_item_information(title, link, 'post__article')    # TODO!
        # print(links)


def parse_item_information(title, link, classname):
    req = requests.get(link)
    if req.status_code == requests.codes.ok:
        soup = BeautifulSoup(req.content, HTML_PARSER)
        content = soup.find('div', attrs={'class': classname})

        content = re.sub("<.*?>", " ", str(content))
        content = content.replace('\n',';')
        content = content.replace('\xa0','')

        contents.append({'title':title, 'link':link, 'content': content})

if __name__ == '__main__':
    get_item_link_list()
    # parse_item_information('3c', 'http://ianchiu1107.pixnet.net/blog/post/402690227', 'article-content-inner')
    # print(contents)
    with open('makeup2.json','w') as f: json.dump(contents, f)
