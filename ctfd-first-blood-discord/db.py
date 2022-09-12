import sqlite3
from typing import List

from challenge import Challenge
from user import User


class DB:
    conn = sqlite3.connect('./data/ctfd-solve-announcer.sqlite')
    cursor = conn.cursor()

    @staticmethod
    def init_db():
        DB.cursor.execute(
            'CREATE TABLE IF NOT EXISTS announced_solves (chal_id integer, user_id integer)'
        )

        DB.conn.commit()

    @staticmethod
    def add_to_db(chal: Challenge, solved_users: List[User]):
        DB.cursor.execute(
            "SELECT user_id FROM announced_solves WHERE chal_id = ?",
            (chal.chal_id, ))
        announced_ids = DB.cursor.fetchall()

        for user in solved_users:
            if user.user_id not in announced_ids:
                DB.cursor.execute("INSERT INTO announced_solves VALUES (?, ?)",
                                  (chal.chal_id, user.user_id))
                DB.conn.commit()
