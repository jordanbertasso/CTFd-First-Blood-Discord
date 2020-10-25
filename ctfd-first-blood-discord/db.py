import sqlite3
import os


class db:
    conn = sqlite3.connect('ctfd-solve-announcer.db')
    cursor = conn.cursor()

    @staticmethod
    def init_db():
        db.cursor.execute(
            'CREATE TABLE IF NOT EXISTS announced_solves (chal_id integer, user_id integer)')

        db.conn.commit()
