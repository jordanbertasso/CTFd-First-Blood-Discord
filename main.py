import asyncio
import requests
import json
import config
from dateutil.parser import isoparser


solved_chals = []

s = requests.Session()
s.headers.update({"Authorization": f"Token {config.api_token}"})


def get_solved_chals(loop):
    res = s.get(config.host + "/statistics/challenges/solves", json=True)

    chals = res.json()["data"]

    for chal in chals:
        id: int = chal["id"]
        solves = chal["solves"]

        if id not in solved_chals and solves > 0:
            solved_chals.append(id)
            chal_name = chal["name"]

            print(f"Challenge: {chal_name} - {id}")

            user_name = get_first_blood_user(id)
            call_webhook(chal_name, user_name)

    loop.call_later(config.poll_period, get_solved_chals, loop)


def get_first_blood_user(chal_id: int) -> str:
    res = s.get(f"{config.host}/challenges/{chal_id}/solves", json=True)

    data = res.json()["data"]

    solves = [{
        "user_id": solve["account_id"],
        "user_name": solve["name"],
        "solve_time": isoparser().isoparse(solve["date"])
    } for solve in data]

    solves.sort(key=lambda x: x["solve_time"].timestamp())

    user_name = solves[0]["user_name"]
    user_id = solves[0]["user_id"]
    print(f"First Blood: {user_name} - {user_id}")

    return user_name


def get_user_team(user_id: int):
    res = s.get(f"{config.host}/users/{user_id}", json=True)
    data = res.json()["data"]


def call_webhook(chal_name: str, user_name: str):
    data = json.loads(s.get(config.webhook_url).content.decode())

    data["content"] = config.announce_string.format(
        user_name=user_name, chal_name=chal_name)

    res = s.post(config.webhook_url, json=data)


def main():
    loop = asyncio.get_event_loop()
    loop.call_soon(get_solved_chals, loop)

    try:
        loop.run_forever()
    finally:
        loop.close()


if __name__ == "__main__":
    main()
