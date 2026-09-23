from flask import g
import mysql.connector

db_config = {
        'host' : '<DB_HOST>',
        'user' : '<DB_USER>',
        'password': '<DB_PASS>',
        'database' : '<DB_NAME>'
        }

def get_db():
    if 'db' not in g:
        g.db = mysql.connector.connect(**db_config)
    return g.db

def close_db(e=None):
    db = g.pop('db',None)
    if db is not None:
        db.close()
