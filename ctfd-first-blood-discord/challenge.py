import logging
from json.decoder import JSONDecodeError
from typing import Dict, cast

import requests
from dateutil.parser import isoparser

from api_session import session as s
from user import User

category_cache: Dict[int, str] = {}


class Challenge():
    chal_id: int
    name: str
    category: str
    num_solves: int

    def __init__(self, chal_id: int, name: str, num_solves: int):
        self.chal_id = chal_id
        self.name = name
        self.num_solves = num_solves

        self._set_category()

    def get_solved_users(self):
        try:
            res = s.get(f"challenges/{self.chal_id}/solves")
        except requests.RequestException as error:
            logging.debug(error)
            return None

        try:
            data = res.json()["data"]
        except (ValueError, JSONDecodeError, KeyError) as error:
            logging.debug(error)
            return None

        solved_users = [
            User(solve["account_id"], solve["name"]) for solve in data
        ]

        return solved_users

    def _set_category(self):
        if self.category is None:
            category = category_cache.get(self.chal_id, None)

            if category is None:
                try:
                    res = s.get(f"challenges/{self.chal_id}")
                    self.category = res.json()["data"]["category"]

                    category_cache[self.chal_id] = self.category
                except requests.RequestException as error:
                    logging.debug(error)

    def get_first_blood_user(self) -> User | None:
        try:
            res = s.get(f"challenges/{self.chal_id}/solves")
        except requests.RequestException as error:
            logging.debug(error)
            return None

        try:
            data = res.json()["data"]
        except (ValueError, JSONDecodeError, KeyError) as error:
            logging.debug(error)
            return None

        solves = [{
            "user_id": solve["account_id"],
            "user_name": solve["name"],
            "solve_time": isoparser().isoparse(solve["date"])
        } for solve in data]

        solves.sort(key=lambda x: x["solve_time"].timestamp())

        user_name = cast(str, solves[0]["user_name"])
        user_id = cast(int, solves[0]["user_id"])
        logging.info("First Blood: %s - %s", user_name, user_id)

        return User(user_id, user_name)
