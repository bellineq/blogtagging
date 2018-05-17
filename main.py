#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from flask import Flask
from flask import jsonify
from flask import render_template
from flask import request
from flask import send_from_directory

import json, os

UPLOAD_FOLDER = 'fig'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# json_file = 'data/3c.json'
# json_file = 'data/makeup.json'
# with open(json_file, 'r') as f:
#     articles = json.load(f)
#     for a in articles: articleList.append([a['id'], a['title']])

@app.route('/', methods=['GET', 'POST'])
def main():
    procedure = os.path.join(app.config['UPLOAD_FOLDER'], 'procedure.png')
    standard = os.path.join(app.config['UPLOAD_FOLDER'], 'standard.png')
    return render_template('home.html', procedure = procedure, standard = standard)

@app.route('/fig/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],filename)

@app.route('/<category>', methods=['GET', 'POST'])
def category(category):

    json_file = 'data/'+str(category)+'_s.json'
    articleList = []
    with open(json_file, 'r') as f: 
        articles_s = json.load(f)
        for a in articles_s: articleList.append([a['id'], a['title']])
    f.close()

    json_file = 'data/'+str(category)+'_w.json'
    with open(json_file, 'r') as f: 
        articles_w = json.load(f)
    f.close()


    index = request.args.get('index')
    if not index: 
        if category == 'tech':
            index = 'S329768706'  # tech
        elif category == 'makeup':
             index = 'q463067765'  # makeup
        elif category == 'movie':
             index = 'H175859823'  # movie
        elif category == 'food':
             index = 'j66802947' # food              
    articleType = str(category)

    for a in articles_s:
        if a['id']==index:
            articleName = a['title']
            articleLink = a['link']
            content_s = a['content']
            break

    for a in articles_w:
        if a['id']==index:
            content_w = a['content']
            break

    return render_template('index.html', article_s=content_s, article_w =content_w, articleIndex=index, articleName=articleName, 
    articleLink=articleLink, articleList=articleList, articleType = articleType)

@app.route('/save', methods=['POST'])
def save():
    try:
        content = request.get_json()

        json_file = 'data/'+content['articleType']+'_w.json'        
        
        with open(json_file, 'r') as f: data = json.load(f)
        for d in data:
            if d['id']==content['index']: d['content']=content['data_w']
        with open(json_file, 'w') as f: json.dump(data, f)
        f.close()

        json_file = 'data/'+content['articleType']+'_s.json'     

        with open(json_file, 'r') as f: data = json.load(f)
        for d in data:
            if d['id']==content['index']: d['content']=content['data_s']
        with open(json_file, 'w') as f: json.dump(data, f)
        f.close()
        
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


# @app.route('/tech', methods=['GET', 'POST'])
# def tech():
#     json_file = 'data/tech.json'
#     articleList = []
#     with open(json_file, 'r') as f: 
#         articles = json.load(f)
#         for a in articles: articleList.append([a['id'], a['title']])
#     index = request.args.get('index')
#     if not index: index = 'S329768706'  # tech
#     articleType = 'tech'
#     for a in articles:
#         if a['id']==index:
#             articleName = a['title']
#             articleLink = a['link']
#             content = a['content']
#             break
#     return render_template('index.html', article=content, articleIndex=index, articleName=articleName, 
#     articleLink=articleLink, articleList=articleList, articleType = articleType)

# @app.route('/makeup', methods=['GET', 'POST'])
# def makeup():
#     json_file = 'data/makeup.json'
#     articleList = []
#     with open(json_file, 'r') as f: 
#         articles = json.load(f)
#         for a in articles: articleList.append([a['id'], a['title']])
#     index = request.args.get('index')
#     print('index:', index)
#     if not index: index = 'q463067765'  # makeup
#     articleType = 'makeup'
#     for a in articles:
#         if a['id']==index:
#             articleName = a['title']
#             articleLink = a['link']
#             content = a['content']
#             break
#     return render_template('index.html', article=content, articleIndex=index, articleName=articleName, 
#     articleLink=articleLink, articleList=articleList, articleType = articleType)

# @app.route('/movie', methods=['GET', 'POST'])
# def movie():
#     json_file = 'data/movie.json'
#     articleList = []
#     with open(json_file, 'r') as f: 
#         articles = json.load(f)
#         for a in articles: articleList.append([a['id'], a['title']])
#     index = request.args.get('index')
#     print('index:', index)
#     if not index: index = 'H175859823'  # movie
#     articleType = 'movie'
#     for a in articles:
#         if a['id']==index:
#             articleName = a['title']
#             articleLink = a['link']
#             content = a['content']
#             break
#     return render_template('index.html', article=content, articleIndex=index, articleName=articleName, 
#     articleLink=articleLink, articleList=articleList, articleType = articleType)

# @app.route('/food', methods=['GET', 'POST'])
# def food():
#     json_file = 'data/food.json'
#     articleList = []
#     with open(json_file, 'r') as f: 
#         articles = json.load(f)
#         for a in articles: articleList.append([a['id'], a['title']])
#     index = request.args.get('index')
#     print('index:', index)
#     if not index: index = 'j66802947' # food
#     articleType = 'food'
#     for a in articles:
#         if a['id']==index:
#             articleName = a['title']
#             articleLink = a['link']
#             content = a['content']
#             break
#     return render_template('index.html', article=content, articleIndex=index, articleName=articleName, 
#     articleLink=articleLink, articleList=articleList, articleType = articleType)

# @app.route('/<category>', methods=['GET', 'POST'])
# def category(category):  
#     json_file = 'data/'+str(category)+'.json'
#     articleList = []
#     with open(json_file, 'r') as f: 
#         articles = json.load(f)
#         for a in articles: articleList.append([a['id'], a['title']])
#     index = request.args.get('index')
#     if not index: 
#         if category == 'tech':
#             index = 'S329768706'  # tech
#         elif category == 'makeup':
#              index = 'q463067765'  # makeup
#         elif category == 'movie':
#              index = 'H175859823'  # movie
#         elif category == 'food':
#              index = 'j66802947' # food              
#     articleType = str(category)
#     for a in articles:
#         if a['id']==index:
#             articleName = a['title']
#             articleLink = a['link']
#             content = a['content']
#             break
#     return render_template('index.html', article=content, articleIndex=index, articleName=articleName, 
#     articleLink=articleLink, articleList=articleList, articleType = articleType)

# def save():
#     try:
#         content = request.get_json()
#         if content['articleType'] == 'tech':
#             json_file = 'data/tech.json'
#         elif content['articleType'] == 'makeup':
#             json_file = 'data/makeup.json'
#         elif content['articleType'] == 'movie':
#             json_file = 'data/movie.json'
#         elif content['articleType'] == 'food':
#             json_file = 'data/food.json'

#         with open(json_file, 'r') as f: data = json.load(f)
#         for d in data:
#             if d['id']==content['index']: d['content']=content['data']
#         with open(json_file, 'w') as f: json.dump(data, f)
#         return jsonify(message='')
#     except Exception as e:
#         print(f'"/save" failed: {e}')
#         return jsonify(message=str(e)), 500