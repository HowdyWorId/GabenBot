import sqlite3


class SQLighter:
    def __init__(self):
        self.conn = sqlite3.connect('database.db')
        self.cur = self.conn.cursor()

    def save(self):
        self.conn.commit()

    def close(self):
        self.conn.close()


