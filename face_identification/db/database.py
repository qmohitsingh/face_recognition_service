import mysql.connector
import pickle
from os import fsync


class Database:
    def __init__(self):
        print('Database obj created...')

    def get_all_embeddings(self, cursor):
        cursor.execute("SELECT * FROM tb_embeddings")
        rows = cursor.fetchall()
        print('rows:', rows)