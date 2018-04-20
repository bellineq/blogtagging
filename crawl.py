import requests, re, json, string, random
from bs4 import BeautifulSoup

HTML_PARSER = "html.parser"
ROOT_URL = 'https://styleme.pixnet.net'                 # TODO!
LIST_URL = 'https://styleme.pixnet.net/makeupsharing'   # TODO!
# LIST_URL = 'https://tech3c.pixnet.net/category/24'        # 3c

contents = []  # 儲存取得的文章資料

def get_item_link_list():
    list_req = requests.get(LIST_URL)
    if list_req.status_code == requests.codes.ok:
        soup = BeautifulSoup(list_req.content, HTML_PARSER)
        articles = soup.find_all('div', attrs={'class': 'article-bg'})  # makeup
# articles = soup.find_all('li', attrs={'class': 'gird-item'})      # 3c

        links = []
        for a in articles:
            link = ROOT_URL+a.find('a')['href']   # makeup
# link = a.find('a')['href']     # 3c
            title = a.find('a', attrs={'class': 'article__content__title--single'}).string  # makeup
# title = a.find('p', attrs={'class': 'gird-item__desc'}).string  # makeup
            links.append({
                'title': title,
                'href': link
            })
            parse_item_information(title, link, 'post__article')    # makeup
# parse_item_information(title, link, 'article-content')    # 3c
        # print(links)


def parse_item_information(title, link, classname):
    req = requests.get(link)
    if req.status_code == requests.codes.ok:
        soup = BeautifulSoup(req.content, HTML_PARSER)
        content = soup.find('div', attrs={'class': classname})

        content = re.sub("<.*?>", " ", str(content))
        content = content.replace('\n',';')
        content = content.replace('\xa0','')
        content_html = ''
        for l_id, line in enumerate(content.split(';')):
            content_html+='<p>'
            for w_id, word in enumerate(line): content_html+='<word id="'+str(l_id)+'-'+str(w_id)+'">'+word+'</word>'
            content_html+='</p>'
        index = random.choice(string.ascii_letters)+link.rsplit('/', 1)[1]
        contents.append({'id':index, 'title':title, 'link':link, 'content': content_html})
        # content = [[(word, f'{l_id:01}-{w_id:01}',) \
            # for w_id, word in enumerate(line)] \
                # for l_id, line in enumerate(content.split(';'))]
        # for line in content:
            # for word in line:
        # contents.append({'title':title, 'link':link, 'content': content})

if __name__ == '__main__':
    get_item_link_list()
#   parse_item_information('【懶人包】筆電選購建議 　 (最後更新：2018.3.29更新)', 'http://ofeyhong.pixnet.net/blog/post/206396230', 'article-content-inner')
#   parse_item_information('【開箱】ASUS VivoBook S15 S510UN 15.6吋/輕薄/高效能/遊戲機/原裝128G SSD+1TB', 'http://ofeyhong.pixnet.net/blog/post/220714371', 'article-content-inner')
#   parse_item_information('【筆電開箱】acer SF514-51-79JE (超高效能的文書機)', 'http://ofeyhong.pixnet.net/blog/post/218181567', 'article-content-inner')
#   parse_item_information('今年中低價位最實用的藍芽喇叭十大排名推薦', 'https://goo.gl/12eHjB', 'article-content-inner')
#   parse_item_information('2017年 十款最佳無線藍牙耳機推薦', 'https://goo.gl/eGjptc', 'article-content-inner')
#   parse_item_information('2017最新十大知名智能手環大評比', 'https://goo.gl/r1WdTy', 'article-content-inner')
#   parse_item_information('「手機選購」破解迷思 手機挑選.購買法則 (2018版)', 'http://aton5918.pixnet.net/blog/post/213841819', 'article-content-inner')
#   parse_item_information('OK Google 超方便的語音傳達指令', 'http://softwarecenter.pixnet.net/blog/post/65582269', 'article-content-inner')
#   parse_item_information('Google 翻譯兩大功能 拍照翻譯、即時翻譯', 'http://softwarecenter.pixnet.net/blog/post/65465098', 'article-content-inner')
#   parse_item_information('USB無線網路卡安裝教學', 'http://softwarecenter.pixnet.net/blog/post/66653616', 'article-content-inner')
# print(contents)
    with open('data/makeup.json','w') as f: json.dump(contents, f)
# with open('data/3c.json','w') as f: json.dump(contents, f)
