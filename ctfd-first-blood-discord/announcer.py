import json
import logging
import time
from json.decoder import JSONDecodeError
from typing import Any, Dict

import requests
from discord import Webhook

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

        webhook = Webhook.from_url(url=self.webhook_url, )

        if first_blood:
            webhook.send(
                self.first_blood_string.format(user_name=user_name,
                                               chal_name=chal_name,
                                               emojis=emoji))
        else:
            webhook.send(
                self.solve_string.format(user_name=user_name,
                                         chal_name=chal_name,
                                         emojis=emoji))
