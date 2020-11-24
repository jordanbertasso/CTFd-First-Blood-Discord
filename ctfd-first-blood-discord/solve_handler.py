import config
import logging
from requests import Session
from dateutil.parser import isoparser
from announcer import Announcer
from challenge import Challenge
from api_session import session as s
from db import db
from json.decoder import JSONDecodeError


class Solve_Handler:
    host: str

    def __init__(self):
        super().__init__()
        self.announcer = Announcer()
    
    def handle_past_solves(self, loop):
        logging.debug("HANDLING PAST SOLVES")

        try:
            res = s.get("statistics/challenges/solves", json=True)
        except:
            loop.call_later(config.poll_period, self.handle_solves, loop)
            return

        try:
            chals = res.json()["data"]
        except (ValueError, JSONDecodeError, KeyError) as e:
            print(e)
            chals = []

        for chal_data in chals:
            chal = Challenge(
                chal_data["id"], chal_data["name"], chal_data["solves"])

            users: [User] = chal.get_solved_users()
            if users:
                db.add_to_db(chal, users)

        loop.call_soon(self.handle_solves, loop)

    def handle_solves(self, loop):
        logging.debug("NEW ROUND")
        try:
            res = s.get("statistics/challenges/solves", json=True)
        except:
            loop.call_later(config.poll_period, self.handle_solves, loop)
            return

        try:
            chals = res.json()["data"]
        except (ValueError, JSONDecodeError, KeyError) as e:
            print(e)
            chals = []

        for chal_data in chals:
            chal = Challenge(
                chal_data["id"], chal_data["name"], chal_data["solves"])

            db.cursor.execute(
                "SELECT user_id FROM announced_solves WHERE chal_id == ?", (chal.id,))
            res = db.cursor.fetchall()
            logging.debug(f"Solvers id's: {res}")
            if not res and chal.num_solves > 0:
                self.handle_first_blood(chal)
            else:
                logging.debug(f"Already announced first blood for {chal.name}")

            if config.announce_all_solves and chal.num_solves > 0:
                try:
                    db.cursor.execute(
                        "SELECT chal_id FROM announced_solves WHERE chal_id == ?", (chal.id, ))
                    res = db.cursor.fetchone()
                    assert res != []
                except AssertionError:
                    logging.error(
                        "Challenge already solved but wasn't announced. Skipping")
                    break

                self.handle_new_solves(chal)

        loop.call_later(config.poll_period, self.handle_solves, loop)

    def handle_first_blood(self, chal: Challenge):
        logging.info(f"Challenge: {chal.name} - {chal.id}")

        user: User = chal.get_first_blood_user()
        if not user:
            return

        db.cursor.execute(
            "INSERT INTO announced_solves VALUES (?, ?)", (chal.id, user.id))
        db.conn.commit()

        self.announcer.announce(chal.name, user.name, first_blood=True)

    def handle_new_solves(self, chal: Challenge):

        users: [User] = chal.get_solved_users()

        if not users:
            return

        db.cursor.execute(
            "SELECT user_id FROM announced_solves WHERE chal_id == ?", (chal.id, ))
        res = db.cursor.fetchall()

        for user in users:
            if (user.id,) not in res:
                logging.info(
                    f"New Solve - Challenge: {chal.name} - User: {user.name}")

                db.cursor.execute(
                    "INSERT INTO announced_solves VALUES (?, ?)", (chal.id, user.id))
                db.conn.commit()
                self.announcer.announce(
                    chal.name, user.name, first_blood=False)
            else:
                logging.debug(
                    f"Already announced solve on {chal.name} by {user.name} - {user.id}")
