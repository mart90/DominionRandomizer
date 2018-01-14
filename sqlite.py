import logging
import sqlite3
from sqlite3 import Error


class Sqlite(object):
    def __init__(self):
        self.conn = None
        self.cursor = None

    def connect(self, dbfilename):
        try:
            self.conn = sqlite3.connect(dbfilename)
            self.cursor = self.conn.cursor()
        except Error as e:
            logging.error(e)

    def commit(self):
        self.conn.commit()

    def close(self):
        self.conn.close()

    def last_inserted_id(self):
        return self.cursor.lastrowid

    def query(self, qry, *args):
        try:
            self.cursor.execute(qry, *args)
        except Error as e:
            logging.error(e)

sql = Sqlite()
