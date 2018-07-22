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
    updateCat('user0', 'food_0, movie_0, beauty_0')
    updateCat('user1', 'food_1, movie_1,tech_0')
    updateCat('user2', 'food_2, movie_2,tech_1')
    updateCat('user3', 'beauty_1, food_3,movie_3')
    updateCat('user4', 'beauty_2, food_4,movie_4')
    updateCat('user5', 'beauty_3, food_5,movie_5')
    updateCat('user6', 'food_6,movie_6')
    view()
    
