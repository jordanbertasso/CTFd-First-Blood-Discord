import sqlite3
import os
from challenge import Challenge
from user import User


class db:
    conn = sqlite3.connect('./data/ctfd-solve-announcer.db')
    cursor = conn.cursor()

    @staticmethod
    def init_db():
        db.cursor.execute(
            'CREATE TABLE IF NOT EXISTS announced_solves (chal_id integer, user_id integer)')

        db.conn.commit()
    
    @staticmethod
    def add_to_db(chal: Challenge, solved_users: [User]):
        db.cursor.execute(
            "SELECT user_id FROM announced_solves WHERE chal_id == ?", (chal.id,))
        announced_ids = db.cursor.fetchall()

        for user in solved_users:
            if user.id not in announced_ids:
                db.cursor.execute(
                    "INSERT INTO announced_solves VALUES (?, ?)", (chal.id, user.id))
                db.conn.commit()
