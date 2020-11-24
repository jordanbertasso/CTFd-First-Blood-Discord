import config
import logging
from dateutil.parser import isoparser
from user import User
from api_session import session as s
from json.decoder import JSONDecodeError


class Challenge():
    id: int
    name: str
    num_solves: int

    def __init__(self, id, name, num_solves):
        self.id = id
        self.name = name
        self.num_solves = num_solves

    def get_solved_users(self):
        try:
            res = s.get(f"challenges/{self.id}/solves", json=True)
        except:
            return None

        try:
            data = res.json()["data"]
        except (ValueError, JSONDecodeError, KeyError) as e:
            print(e)
            return []

        solved_users = [User(solve["account_id"], solve["name"])
                        for solve in data]

        return solved_users

    def get_first_blood_user(self) -> User:
        try:
            res = s.get(f"challenges/{self.id}/solves", json=True)
        except:
            return None

        try:
            data = res.json()["data"]
        except (ValueError, JSONDecodeError, KeyError) as e:
            print(e)
            return None

        solves = [{
            "user_id": solve["account_id"],
            "user_name": solve["name"],
            "solve_time": isoparser().isoparse(solve["date"])
        } for solve in data]

        solves.sort(key=lambda x: x["solve_time"].timestamp())

        user_name = solves[0]["user_name"]
        user_id = solves[0]["user_id"]
        logging.info(f"First Blood: {user_name} - {user_id}")

        return User(user_id, user_name)
