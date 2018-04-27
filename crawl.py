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
    # get_item_link_list()
    parse_item_information('高C/P值的平民散熱神器~LEPA利豹LPALV12風冷塔式散熱器開箱心得分享', 'http://redcell6.pixnet.net/blog/post/33656192', 'article-content-inner')
    parse_item_information('ASUS ZenBook 13(UX331ULA) 美•力隨型 不到 1kg 的 13 吋超輕薄體驗', 'http://www.fox-saying.com/blog/post/45782040', 'article-content-inner')
    parse_item_information('三軸穩定器，我只推薦最強的SwiftCam M4', 'http://ysyyu.pixnet.net/blog/post/43918914-%E4%B8%89%E8%BB%B8%E7%A9%A9%E5%AE%9A%E5%99%A8%EF%BC%8C%E6%88%91%E5%8F%AA%E6%8E%A8%E8%96%A6%E6%9C%80%E5%BC%B7%E7%9A%84swiftcam-m4', 'article-content-inner')
    parse_item_information('輕鬆享受就在這一杯，Nespresso Essenza mini自動膠囊咖啡機', 'http://ysyyu.pixnet.net/blog/post/43761793-%E8%BC%95%E9%AC%86%E4%BA%AB%E5%8F%97%E5%B0%B1%E5%9C%A8%E9%80%99%E4%B8%80%E6%9D%AF%EF%BC%8Cnespresso-essenza-mini%E8%87%AA%E5%8B%95', 'article-content-inner')
    parse_item_information('[電腦零件選購] 主機板 挑選.選購法則 V2.2新版', 'http://aton5918.pixnet.net/blog/post/213507130', 'article-content-inner')
    parse_item_information('【攻略】旅かえる(旅行青蛙)★朋友攻略大全', 'http://apple83411.pixnet.net/blog/post/198866271-%E3%80%90%E6%94%BB%E7%95%A5%E3%80%91%E6%97%85%E3%81%8B%E3%81%88%E3%82%8B%28%E6%97%85%E8%A1%8C%E9%9D%92%E8%9B%99%29%E2%98%85%E6%9C%8B%E5%8F%8B%E5%96%9C%E6%84%9B%E7%89%A9%E5%93%81', 'article-content-inner')
    parse_item_information('Sdorica -sunset-（萬象物語）四個月玩後感', 'http://catchtest.pixnet.net/blog/post/32259718-sdorica--sunset-%EF%BC%88%E8%90%AC%E8%B1%A1%E7%89%A9%E8%AA%9E%EF%BC%89%E5%9B%9B%E5%80%8B%E6%9C%88%E7%8E%A9%E5%BE%8C%E6%84%9F', 'article-content-inner')
    parse_item_information('安博盒子三代 使用半年後心得分享', 'http://roadschen.pixnet.net/blog/post/55830021-%E5%AE%89%E5%8D%9A%E7%9B%92%E5%AD%90%E4%B8%89%E4%BB%A3-%E4%BD%BF%E7%94%A8%E5%8D%8A%E5%B9%B4%E5%BE%8C%E5%BF%83%E5%BE%97%E5%88%86%E4%BA%AB', 'article-content-inner')
    parse_item_information('2017最新十大知名智能手環推薦大評比。到底該如何選擇??', 'http://shandy520.pixnet.net/blog/post/146179997-2017%E6%9C%80%E6%96%B0%E5%8D%81%E5%A4%A7%E7%9F%A5%E5%90%8D%E6%99%BA%E8%83%BD%E6%89%8B%E7%92%B0%E5%A4%A7%E8%A9%95%E6%AF%94%E3%80%82%E5%88%B0%E5%BA%95%E8%A9%B2%E5%A6%82', 'article-content-inner')
    # with open('data/makeup.json','w') as f: json.dump(contents, f)
    with open('data/3c2.json','w') as f: json.dump(contents, f)
