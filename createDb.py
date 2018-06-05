import sqlite3
import csv

with open('./data/user.csv', newline='') as f:
    csv_reader = csv.DictReader(f)
    user = [(row['username'], row['password']) for row in csv_reader]

with open('schema.sql') as f:
    sql = f.read()

db = sqlite3.connect('user.db')
with db:
    db.executescript(sql)
    db.executemany(
        'INSERT INTO  user (username, password) VALUES (?, ?)', user
    )