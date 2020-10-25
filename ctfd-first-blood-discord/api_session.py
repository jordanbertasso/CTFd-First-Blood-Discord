import config
from urllib.parse import urljoin, urlparse
from requests import Session


class API_Session(Session):
    host: str

    def __init__(self):
        super().__init__()
        self.headers.update(
            {"Authorization": f"Token {config.api_token}", "Accept": "application/json"})
        self.host = config.host
        parsed = urlparse(config.host)
        self.endpoint = urljoin(parsed.geturl(), "/api/v1/")

    def get(self, url, params=None, **kwargs):
        if url[0] == "/":
            url = url[1:]

        url = urljoin(self.endpoint, url)
        return super().get(url, params=params, **kwargs)


session = API_Session()
