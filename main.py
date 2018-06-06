#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from flask import (
    Flask, jsonify, render_template, request, send_from_directory, url_for, 
    g, redirect, session, 
)
import json, os, sqlite3

app = Flask(__name__)
SQLITE_DB_PATH = 'user.db'
SQLITE_DB_SCHEMA = 'schema.sql'
MEMBER_CSV_PATH = './data/user.csv'
app.secret_key = 'd7e977e3b75db569238259291645ceefde9dd89c3c6a5365'

@app.route('/', methods=['GET', 'POST'])
def main():
    return render_template('home.html')

@app.route('/category/<category>', methods=['GET', 'POST'])
def category(category):
    ##  locate json file
    json_file = getJsonLoc(category)    

    ##  collect info for all articles in the category
    articleList = []
    articleType = category
    with open(json_file, 'r', encoding="utf-8") as f: 
        articles = json.load(f)
        for a in articles: articleList.append([a['id'], a['title'], a['number']])
    f.close()

    ## collect data for specific article
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
            if 'status' not in a:
                a['status'] = 'untagged'
            status = a['status']
            break

    ##  specify allowed article status        
    statusList = ['untagged','tagging','tagged','abandoned']

    return render_template('index.html', article_s=content_s, article_w=content_w, 
    articleIndex=index, articleName=articleName, articleLink=articleLink,
    articleList=articleList, articleType=articleType, view_count=view_count, word_count = word_count,
    item_name = item_name, item_store = item_store, articleStatus = status, statusList=statusList)


@app.route('/articlelist/<category>', methods=['GET', 'POST'])
def articleList(category):
    ##  locate json file
    json_file = getJsonLoc(category) 
    
    ## collect info for all articles in the category
    articleList = []
    articleType = category
    with open(json_file, 'r', encoding="utf-8") as f: 
        articles = json.load(f)
        for a in articles: 
            if 'status' not in a:
                a['status'] = 'untagged'
            articleList.append([a['id'], a['title'], a['number'], a['status']])
    f.close()
    
    return render_template('articleList.html', articleList=articleList, articleType=articleType)

@app.route('/save', methods=['POST'])
def save():
    try:
        ## get data from user
        content = request.get_json()
        articleType = content['articleType']

        ## locate json file
        json_file = getJsonLoc(articleType) 
        
        with open(json_file, 'r', encoding="utf-8") as f: data = json.load(f)
        for d in data:
            if d['id']==content['index']: 
                d['content_w'] = content['data_w']
                d['content_s'] = content['data_s']
                d['item_name'] = content['item_name']
                d['item_store'] = content['item_store']
                d['status'] = content['status']
        with open(json_file, 'w') as f: json.dump(data, f)
        f.close()
        return jsonify(message='')
    except Exception as e:
        # print(f'"/save" failed: {e}')
        return jsonify(message=str(e)), 500

@app.route('/login', methods=(['GET', 'POST']))
def login():
    try:
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = '帳號或密碼錯誤'
        elif not user[2] == password:
            error = '帳號或密碼錯誤'

        if error is None:
            session.clear()
            session['user_id'] = user[0]
            return redirect(url_for('main'))

        return render_template('login.html', loginError=error)
    except Exception as e:
        print(f'"/log" failed: {e}')
        return redirect(url_for('main'))


@app.before_request
def load_logged_in_user():
    ## obtain user info before every request
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()
        g.categoryList = g.user[3].replace(" ", "").split(",")
        g.username = g.user[1]

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main'))

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(SQLITE_DB_PATH)
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def getJsonLoc(category):
    try:
        if g.username and category:
            return os.path.join('userData', str(g.username), str(category)+'.json')    
        else:
            return os.path.join('data', str(category)+'.json')
    except:
        return os.path.join('data', str(category)+'.json')


if __name__ == '__main__':
    # app.run(debug=True, host='140.112.90.203', port=5511)
    app.run(debug=True)
