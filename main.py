#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from flask import Flask
from flask import jsonify
from flask import render_template
from flask import request

import json

app = Flask(__name__)
json_file = 'data/3c_2.json'
json_file_tagged = 'data/3c_tagged.json'
json_file_tags = 'data/3c_tags.json'
tags=[]
articles = []
articleList = []
with open(json_file, 'r') as f: articles = json.load(f)
for i in range(len(articles)): articleList.append([i, articles[i]['title']])

@app.route('/', methods=['GET', 'POST'])
def main():
    page = int(request.args.get('pages'))
    articleName = articles[page]['title']
    articleLink = articles[page]['link']
    a = articles[page]['content']
    return render_template('index.html', article=a, articleIndex=page, articleName=articleName, articleLink=articleLink, articleList=articleList)

@app.route('/page')
def load():
    try:
        print (request.is_json)
        content = request.get_json()
        i = int(content['page'])
        print(articles[i])
        articleName = articles[i]['title']
        articleLink = articles[i]['link']
        a = articles[i]

    except Exception as e:
        print(f'"/page" failed: {e}')
        return jsonify(message=str(e)), 500
    return render_template('index.html', article=a, articleName=articleName, articleLink=articleLink, articleList=articleList)

@app.route('/save', methods=['POST'])
def save():
    try:
        content = request.get_json()
        # print(content)
        # print(content['tags'])
        with open(json_file_tagged, 'a') as f: f.write(json.dumps(content)+'\n')
        return jsonify(message='')
    except Exception as e:
        print(f'"/save" failed: {e}')
        return jsonify(message=str(e)), 500

if __name__ == '__main__':
    app.run(debug=True)


# preprocessing code
# plain_article = ';;;    今天來跟大家分享一台由義大利飛雅特集團所設計的電動滑板車，因其台灣代理商的老闆剛好是我大學學長，我才能藉由這個因緣際會很幸運的接觸到這台既方便又實用的電動滑板車。其實它會吸引到我，是因為我平日上班以捷運為主要交通工具，我家雖然位於中和景安站附近，但走路過去差不多也有10分鐘的距離，有時下班已經很累了，出站之後一想到還要用走的回家頓時心又更加疲憊；若是等候接駁車的時間我用走的應該已經到家了，這時若有一台攜帶方便的交通工具便可解決我通勤的問題，而飛雅特FIAT500電動滑板車的出現解決了我由捷運站到家這一段路程的問題。    ;     通勤省錢?     ;    當然可能大家會問，那騎腳踏車或小折不是也可以解決這個問題嗎?對！沒有錯。但我考量的還是通勤的成本，台北捷運之前有個公告： 腳踏車採人車合併收費，單趟不限里程，一律全票收費，攜帶自行車單程票每張收費   新臺幣 80 元   整，旅客請先至車站詢問處向站務人員購票，每張車票僅限 1 人攜帶 1 輛自行車使用，出站回收。 若每天上班牽台自行車上捷運來回成本就是160元。台北捷運還有一條關於小折的注意事項：  旅客將   自行車摺疊或拆卸完成並妥善包裝後   （惟包裝後之最長邊不得超過165公分，且長、寬、高之和不得超過220公分），即可比照一般行李，攜入各捷運車站乘車，無開放時段之限制。  而小折當然就是體積大、折疊不易等等惱人的問題。於是飛雅特FIAT500電動滑板車真的是最佳的解決方案。    ;         ;  ;     媒體和玩家眼中的時尚品牌 飛雅特設計     ;    我們先來看它的外觀設計，它是由義大利飛雅特集團所操刀設計的，其 旗下的品牌包括蘭吉雅（Lancia）、阿爾法·羅密歐（Alfa Romeo）和瑪莎拉蒂（Maserati）及法拉利（Ferrari）等汽車品牌，也難怪看到它第一眼時，就被它的時尚造型所深深吸引。     ;         ;  ;    高強度鋁合金的車身，除了強化了產品本身的質感，也讓整體的重量變得極為輕巧僅6.9KG。    ;         ;  ;    在止滑踏板方面的處理也極為用心，一整面的塑膠粗咬花加強止滑度，使得騎乘更為安全。    ;'
# for r in raw_articles:
#     article = [[(word, f'{l_id:01}-{w_id:01}',) \
#         for w_id, word in enumerate(line)] \
#             for l_id, line in enumerate(r['content'].split(';'))]
