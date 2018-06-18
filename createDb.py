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
    updateCat('user0', 'beautymakeup_0,food_0,moviecritics_0')
    updateCat('user1', 'tech_0,food_1,moviecritics_1')
    updateCat('user2', 'tech_1,food_2,moviecritics_2')
    updateCat('user3', 'beautymakeup_1,food_3,moviecritics_3')
    updateCat('user4', 'beautymakeup_2,food_4,moviecritics_4')
    view()
    