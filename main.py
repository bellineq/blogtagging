#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from flask import Flask
from flask import jsonify
from flask import render_template
from flask import request

import json

app = Flask(__name__)
# json_file = 'data/3c.json'
# json_file = 'data/makeup.json'
# with open(json_file, 'r') as f:
#     articles = json.load(f)
#     for a in articles: articleList.append([a['id'], a['title']])

@app.route('/', methods=['GET', 'POST'])
def main():
    return render_template('home.html')

@app.route('/tech', methods=['GET', 'POST'])
def tech():
    json_file = 'data/tech.json'
    articleList = []
    with open(json_file, 'r') as f: 
        articles = json.load(f)
        for a in articles: articleList.append([a['id'], a['title']])
    index = request.args.get('index')
    if not index: index = 'l206396230'  # 3c
    articleType = 'tech'
    for a in articles:
        if a['id']==index:
            articleName = a['title']
            articleLink = a['link']
            content = a['content']
            break
    return render_template('index.html', article=content, articleIndex=index, articleName=articleName, 
    articleLink=articleLink, articleList=articleList, articleType = articleType)

@app.route('/makeup', methods=['GET', 'POST'])
def makeup():
    json_file = 'data/makeup.json'
    articleList = []
    with open(json_file, 'r') as f: 
        articles = json.load(f)
        for a in articles: articleList.append([a['id'], a['title']])
    index = request.args.get('index')
    print('index:', index)
    if not index: index = 'v221808882'  # makeup
    articleType = 'makeup'
    for a in articles:
        if a['id']==index:
            articleName = a['title']
            articleLink = a['link']
            content = a['content']
            break
    return render_template('index.html', article=content, articleIndex=index, articleName=articleName, 
    articleLink=articleLink, articleList=articleList, articleType = articleType)


@app.route('/save', methods=['POST'])
def save():
    try:
        content = request.get_json()
        if content['articleType'] == 'tech':
            json_file = 'data/tech.json'
        elif content['articleType'] == 'makeup':
            json_file = 'data/makeup.json'
        with open(json_file, 'r') as f: data = json.load(f)
        for d in data:
            if d['id']==content['index']: d['content']=content['data']
        with open(json_file, 'w') as f: json.dump(data, f)
        return jsonify(message='')
    except Exception as e:
        print(f'"/save" failed: {e}')
        return jsonify(message=str(e)), 500

if __name__ == '__main__':
    app.run(debug=True)


# @app.route('/article/{articleIndex}')
# def article(articleIndex):
#     index = int(articleIndex)
#     return str(articles[index]['content'])

# @app.route('/page')
# def load():
#     try:
#         # print (request.is_json)
#         content = request.get_json()
#         i = content['index']
#         # print(articles[i])
#         articleName = articles[i]['title']
#         articleLink = articles[i]['link']
#         a = articles[i]
#
#     except Exception as e:
#         print(f'"/page" failed: {e}')
#         return jsonify(message=str(e)), 500
#     return render_template('index.html', article=a, articleName=articleName, articleLink=articleLink, articleList=articleList)

# with open(json_file_tagged, 'a') as f: f.write(json.dumps(content)+'\n')
