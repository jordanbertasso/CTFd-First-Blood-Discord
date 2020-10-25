import config
import logging
from requests import Session
from dateutil.parser import isoparser
from announcer import Announcer
from challenge import Challenge
from api_session import session as s


class Solve_Handler:
    host: str
    announced_solves: {"chal_id": ["user_ids"]}

    def __init__(self):
        super().__init__()
        self.announced_solves = {}
        self.announcer = Announcer()

    def handle_solves(self, loop):
        logging.info("NEW ROUND")
        res = s.get("statistics/challenges/solves", json=True)

        chals = res.json()["data"]

        for chal_data in chals:
            chal = Challenge(
                chal_data["id"], chal_data["name"], chal_data["solves"])

            if chal.id not in self.announced_solves.keys() and chal.num_solves > 0:
                self.handle_first_blood(chal)
            else:
                logging.debug(f"Already announced first blood for {chal.name}")

            if config.announce_all_solves and chal.num_solves > 0:
                try:
                    assert chal.id in self.announced_solves.keys()
                except AssertionError:
                    logging.error(
                        "Challenge already solved but wasn't announced. Skipping")
                    break

                self.handle_new_solves(chal)

        loop.call_later(config.poll_period, self.handle_solves, loop)

    def handle_first_blood(self, chal: Challenge):
        logging.info(f"Challenge: {chal.name} - {chal.id}")

        user: User = chal.get_first_blood_user()

        self.announced_solves[chal.id] = [user.id]

        self.announcer.announce(chal.name, user.name, first_blood=True)

    def handle_new_solves(self, chal: Challenge):

        users: [User] = chal.get_solved_users()

        for user in users:
            if user.id not in self.announced_solves[chal.id]:
                logging.info(
                    f"New Solve - Challenge: {chal.name} - User: {user.name}")
                self.announced_solves[chal.id].append(user.id)
                self.announcer.announce(
                    chal.name, user.name, first_blood=False)
            else:
                logging.debug(
                    f"Already announced solve on {chal.name} by {user.name}")
