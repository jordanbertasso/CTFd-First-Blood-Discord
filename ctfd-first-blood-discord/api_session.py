from typing import Any, Dict
from urllib.parse import urljoin, urlparse

from requests import Response, Session

import config


class APISession(Session):
    host: str

    def __init__(self):
        super().__init__()
        self.headers.update({
            "Authorization": f"Token {config.API_TOKEN}",
            "Accept": "application/json",
            "Content-Type": "application/json"
        })
        self.host = config.HOST
        parsed = urlparse(config.HOST)
        self.endpoint = urljoin(parsed.geturl(), "/api/v1/")

    def get(self,
            url: str,
            params: Any = None,
            **kwargs: Dict[str, Any]) -> Response:
        if url[0] == "/":
            url = url[1:]

        url = urljoin(self.endpoint, url)
        return super().get(url, params=params, **kwargs)


session = APISession()
