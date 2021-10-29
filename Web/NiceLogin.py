import sqlite3
from time import sleep
from random import randint

conn = sqlite3.connect('APP.db', check_same_thread=False)
cursor = conn.cursor()

def getUserData(username):
    '''Devuelve los datos del usuario'''
    cmd = f'''SELECT * FROM users WHERE username = '{username}' '''
    cursor.execute(cmd)
    data = cursor.fetchone()
    return data if data is not None else None