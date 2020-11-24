import requests
import json
import config
import time
import logging
from json.decoder import JSONDecodeError


class Announcer:
    webhook_data: dict
    solve_string: str
    first_blood_string: str
    rate_limit_remaining: int
    rate_limit_sleep_time: int

    def __init__(self):
        self.webhook_url = config.webhook_url
        self.solve_string = config.solve_announce_string
        self.first_blood_string = config.first_blood_announce_string
        self.webhook_data = json.loads(
            requests.get(self.webhook_url).content.decode())
        self.rate_limit_remaining = 1
        self.rate_limit_sleep_time = 0

    def announce(self, chal_name: str, user_name: str, first_blood=False):
        self.check_rate_limits()

        if first_blood:
            self.webhook_data["content"] = self.first_blood_string.format(
                user_name=user_name, chal_name=chal_name)
        else:
            self.webhook_data["content"] = self.solve_string.format(
                user_name=user_name, chal_name=chal_name)

        res = requests.post(self.webhook_url, json=self.webhook_data)

        # Unavoidable and unpredictable webhook specific rate-limit from Discord
        # Retry if limited
        # https://github.com/discord/discord-api-docs/issues/1454
        self.check_429(res)

        self.update_rate_limits(res)

    def update_rate_limits(self, res):
        try:
            self.rate_limit_remaining = min(
                int(res.headers["X-RateLimit-Remaining"]), int(res.headers["X-RateLimit-Global"]))
        except KeyError:
            self.rate_limit_remaining = int(
                res.headers["X-RateLimit-Remaining"])

        self.rate_limit_sleep_time = int(
            res.headers["X-RateLimit-Reset-After"])

        logging.debug(f"Bucket {res.headers['X-RateLimit-Bucket']}")
        logging.debug(res.status_code)
        logging.debug(f"{self.rate_limit_remaining=}")
        logging.debug(f"{self.rate_limit_sleep_time=}")

    def check_rate_limits(self):
        if self.rate_limit_remaining == 0:
            secs = self.rate_limit_sleep_time
            logging.info(f"Sleeping for {secs}s - Rate Limits\n")
            time.sleep(secs)

    def check_429(self, res):
        if res.status_code == 429:    

            try:
                json = logging.debug(res.json())
                self.rate_limit_sleep_time = json["retry_after"]/1000
            except (ValueError, JSONDecodeError, KeyError) as e:
                print(e)
                self.rate_limit_sleep_time = 60

            logging.info(
                f"429 Received - Sleeping for {self.rate_limit_sleep_time}s")
            time.sleep(self.rate_limit_sleep_time)
            res = requests.post(self.webhook_url, json=self.webhook_data)
