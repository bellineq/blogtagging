#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from flask import Flask
from flask import jsonify
from flask import render_template
from flask import request
from flask import send_from_directory
from flask import url_for

import json, os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def main():
    return render_template('home.html')

@app.route('/category/<category>', methods=['GET', 'POST'])
def category(category):

    json_file = os.path.join('data', str(category)+'.json')
    articleList = []
    articleType = category
    with open(json_file, 'r') as f: 
        articles = json.load(f)
        for a in articles: articleList.append([a['id'], a['title']])
    f.close()

    index = request.args.get('index')
    if not index: 
        index = articles[0]['id']   

    for a in articles:
        if a['id']==index:
            articleName = a['title']
            articleLink = a['link']
            content_s = a['content_s']
            content_w = a['content_w']
            item_name = a['item_name']
            item_store = a['item_store']
            view_count = a['view_count']
            word_count = a['word_count']
            break
    return render_template('index.html', article_s=content_s, article_w =content_w, 
    articleIndex=index, articleName=articleName, articleLink=articleLink, 
    articleList=articleList, articleType=articleType, view_count=view_count, word_count = word_count,
    item_name = item_name, item_store = item_store)


@app.route('/articlelist/<category>', methods=['GET', 'POST'])
def articleList(category):

    json_file = os.path.join('data', str(category)+'.json')
    articleList = []
    articleType = category
    with open(json_file, 'r') as f: 
        articles = json.load(f)
        for a in articles: articleList.append([a['id'], a['title']])
    f.close()
    return render_template('articleList.html', articleList=articleList, articleType=articleType)

@app.route('/save', methods=['POST'])
def save():
    try:
        content = request.get_json()
        articleType = content['articleType']

        json_file = os.path.join('data', articleType+'.json')  
        with open(json_file, 'r') as f: data = json.load(f)
        for d in data:
            if d['id']==content['index']: 
                d['content_w'] = content['data_w']
                d['content_s'] = content['data_s']
                d['item_name'] = content['item_name']
                d['item_store'] = content['item_store']
        with open(json_file, 'w') as f: json.dump(data, f)
        f.close()
        return jsonify(message='')
    except Exception as e:
        # print(f'"/save" failed: {e}')
        return jsonify(message=str(e)), 500

if __name__ == '__main__':
    app.run(debug=True)

