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
    updateCat('user7', 'tech_7, beauty_7')
    updateCat('user8', 'tech_8, moviecritics_8')
    updateCat('user9', 'moviecritics_9')
    updateCat('user10', 'tech_10, moviecritics_10')
    updateCat('user11', 'beauty_11')
    updateCat('user12', 'beauty_12')
    updateCat('user13', 'tech_13, beauty_13, moviecritics_13')
    updateCat('user14', 'beauty_14, moviecritics_14')
    updateCat('user15', 'tech_15, beauty_15, moviecritics_15')
    updateCat('user16', 'beauty_16')
    updateCat('user17', 'moviecritics_17')
    updateCat('user18', 'beauty_18, moviecritics_18')
    updateCat('user19', 'beauty_19, moviecritics_19')
    updateCat('user20', 'tech_20, beauty_20, moviecritics_20')
    view()
    
