from pyloggor import pyloggor
from DisWrap.main import Client
import json
import socket


class Minion:
    def __init__(self, config, logger: pyloggor):
        self.config = config
        self.token = config["token"]
        self.logger = logger

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.handler_addr = ("localhost", config["handler_port"])

        self.dis_client = Client()

        self.__boot()


    def __boot(self):
        self.logger.log("DEBUG", "Boot Sequence", msg="Verifying token and account info", file="DisWrap:Client")

        account_info = self.dis_client.get_info()
        if not account_info:
            message = {"op": "0", "data": {"valid": False, "token": self.token}}
            self.sock.sendto(bytes(json.dumps(message), "utf-8"), self.handler_addr)
            return

        ws_message = {
            "op": "0",
            "event": "IDENTIFY",
            "data": {
                "valid": True,
                "token": self.token,
                "username": account_info["username"],
                "id": account_info["id"],
                "discriminator": account_info["discriminator"],
            }
        }

        self.sock.sendto(bytes(json.dumps(ws_message), "UTF-8"), self.handler_addr)
