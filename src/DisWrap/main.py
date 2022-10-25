import json
import faster_than_requests as requests
from typing import Optional
from .Classes import Response
from pyloggor import pyloggor


class Client:
    def __init__(self, config, logger: pyloggor):
        self.config = config
        self.token = config["token"]
        self.logger = logger


    def get_info(self) -> Optional[dict[str, str]]:
        info = Response(
            requests.get(
                url="https://discord.com/api/v10/users/@me",
                http_headers=[("Authorization", self.token)]
            )
        )

        if info.code != 200:
            return False

        data_json = json.loads(info.data)
        return data_json
