import faster_than_requests as requests
from typing import Optional, TypeVar, Union
from .Objects import Response
from .ws import Gateway
from pyloggor import pyloggor
from string import printable

T: TypeVar = Optional[Union[str, int]]


class Client:
    def __init__(self, config, logger: pyloggor):
        self.config = config

        self.token = config["token"]
        self.logger = logger

        self.gateway = Gateway(config, logger)
        self.ws = self.gateway.ws

        self.session_id: Optional[str] = self.gateway.session_id


    def _strip(self, content: str) -> str:
        return "".join([char for char in content if char in printable])

    def _tupalize(self, dict):
        return [(a, b) for a, b in dict.items()]


    def get_info(self) -> Response:
        return Response(
            requests.get(
                url="https://discord.com/api/v10/users/@me",
                http_headers=[("Authorization", self.token)]
            )
        )

    def send_message(self, content: str, channel_override: T = None) -> tuple[Response, T]:
        if self._strip(content) == "":
            return False

        channel_id = channel_override if channel_override else self.config["channel_id"]
        return Response(
            requests.post(
                url=f"https://discord.com/api/v9/channels/{channel_id}/messages",
                http_headers=[("Authorization", self.token)],
                body="",
                multipart_data=[("content", content)]
            )
        ), channel_override

    def interact(self, payload, retries=25) -> Optional[Response]:
        payload["session_id"] = self.session_id

        for i in range(retries):
            res = Response(
                requests.post(
                    url="https://discord.com/api/v9/interactions",
                    http_headers=[("Authorization", self.token)],
                    body="",
                    multipart_data=self._tupalize(payload)
                )
            )

            if res.code == 429:
                continue

            if res.code == 204:
                return True

            if res.code in (400, 401, 500):
                return res

        return False