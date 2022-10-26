from pyloggor import pyloggor
from DisWrap.main import Client
from typing import Literal
import json
import socket


class Minion:
    def __init__(self, config, logger: pyloggor):
        self.config = config
        self.token = config["token"]
        self.logger = logger

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.handler_addr = ("localhost", config["internal"]["handler_port"])

        self.dis_client = Client()

        self.__boot()
        self.interrupts = []
        self.running_interrupts = False
        self.ongoing_interaction = False

        self.coins = 0
        self.items = {}


    def __boot(self):
        self.logger.log("DEBUG", "Boot Sequence", msg="Verifying token and account info", file="DisWrap:Client")

        account_info = self.dis_client.get_info()
        if account_info.code != 200:
            message = {"op": 0, "data": {"valid": False, "token": self.token}}
            self.sock.sendto(bytes(json.dumps(message), "utf-8"), self.handler_addr)
            return

        data = json.loads(account_info.data)
        ws_message = {
            "op": 0,
            "data": {
                "valid": True,
                "token": self.token,
                "username": data["username"],
                "id": data["id"],
                "discriminator": data["discriminator"],
            }
        }

        self.account_id = data["id"]
        self.acount_username = data["username"]
        self.account_discriminator = data["discriminator"]

        self.sock.sendto(bytes(json.dumps(ws_message), "UTF-8"), self.handler_addr)

        while True:
            message = json.loads(self.sock.recv(1024).decode("UTF-8"))
            if message["op"] == 2:
                self.interrupts.append(message["data"])
                self._interrupt()


    def _interrupt(self):
        if self.running_interrupts:
            return
        """Execute commands from self.running_interrupts."""
    
    def _update_dankinfo(self, coins=None, items=None) -> None:
        self.coins = self.coins + coins if coins else self.coins
        if items:
            for _item, _quan in items.items():
                self.items[_item] = _quan

        message = {
            "op": 1,
            "data": {
                "id": self.account_id,
                "coins": self.coins,
                "items": self.items,
            }
        }

        self.sock.sendto(bytes(json.dumps(message), "UTF-8"), self.handler_addr)
