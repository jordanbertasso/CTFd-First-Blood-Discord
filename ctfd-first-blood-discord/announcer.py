import json
import logging
import time
from json.decoder import JSONDecodeError
from typing import Any, Dict

import requests

import config


class Announcer:
    webhook_data: Dict[str, Any]
    solve_string: str
    first_blood_string: str
    rate_limit_remaining: int
    rate_limit_sleep_time: int

    def __init__(self):
        self.webhook_url = config.WEBHOOK_URL
        self.solve_string = config.SOLVE_ANNOUNCE_STRING
        self.first_blood_string = config.FIRST_BLOOD_ANNOUNCE_STRING
        self.webhook_data = json.loads(
            requests.get(self.webhook_url).content.decode())
        self.rate_limit_remaining = 1
        self.rate_limit_sleep_time = 0

    def announce(self,
                 chal_name: str,
                 user_name: str,
                 emoji: str,
                 first_blood: bool = False):
        self.check_rate_limits()

        if first_blood:
            self.webhook_data["content"] = self.first_blood_string.format(
                user_name=user_name, chal_name=chal_name, emojis=emoji)
        else:
            self.webhook_data["content"] = self.solve_string.format(
                user_name=user_name, chal_name=chal_name, emojis=emoji)

        res = requests.post(self.webhook_url, json=self.webhook_data)

        # Unavoidable and unpredictable webhook specific rate-limit from Discord
        # Retry if limited
        # https://github.com/discord/discord-api-docs/issues/1454
        self.check_429(res)

        self.update_rate_limits(res)

    def update_rate_limits(self, res: requests.Response):
        try:
            self.rate_limit_remaining = min(
                int(res.headers["X-RateLimit-Remaining"]),
                int(res.headers["X-RateLimit-Global"]))
        except KeyError:
            self.rate_limit_remaining = int(
                res.headers["X-RateLimit-Remaining"])

        self.rate_limit_sleep_time = int(
            res.headers["X-RateLimit-Reset-After"])

        logging.debug("Bucket %s", res.headers['X-RateLimit-Bucket'])
        logging.debug(res.status_code)
        logging.debug("rate_limit_remaining=%d", self.rate_limit_remaining)
        logging.debug("rate_limit_sleep_time=%d", self.rate_limit_sleep_time)

    def check_rate_limits(self):
        if self.rate_limit_remaining == 0:
            secs = self.rate_limit_sleep_time
            logging.info("Sleeping for %ds - Rate Limits\n", secs)
            time.sleep(secs)

    def check_429(self, res: requests.Response):
        if res.status_code == 429:

            try:
                data = res.json()
                self.rate_limit_sleep_time = data["retry_after"] / 1000
            except (ValueError, JSONDecodeError, KeyError, TypeError) as error:
                logging.error(error)
                self.rate_limit_sleep_time = 60

            logging.info("429 Received - Sleeping for %ds",
                         self.rate_limit_sleep_time)
            time.sleep(self.rate_limit_sleep_time)
            res = requests.post(self.webhook_url, json=self.webhook_data)
