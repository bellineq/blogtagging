import sqlite3
import csv

def create():
    with open('./data/user.csv', newline='') as f:
        csv_reader = csv.DictReader(f)
        user = [(row['username'], row['password'], '') for row in csv_reader]

    with open('schema.sql') as f:
        sql = f.read()

    db = sqlite3.connect('user.db')
    with db:
        db.executescript(sql)
        db.executemany(
            'INSERT INTO  user (username, password, category) VALUES (?, ?, ?)', user
        )

def view():
    db = sqlite3.connect('user.db')
    with db:
        data = db.execute('SELECT * FROM user')
    for row in data:
        print(row)

def updateCat(user, category):
    db = sqlite3.connect('user.db')
    with db:
        db.execute(
            'UPDATE user SET category = ?  WHERE username= ? ',
            (category, user)
        )

def example():
## this is an example showing how to update category list for user 'guest'
    updateCat('user0', 'tech_0')

if  __name__ == '__main__':
    updateCat('user24', 'movie_24, tech_24')
    updateCat('user25', 'movie_25, beauty_25')
    view()
    
