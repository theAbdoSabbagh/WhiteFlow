from pyloggor import pyloggor
from internals import DankInfoLive
import socket
import json


class Handler:
    def __init__(self, config: dict[str, str], logger: pyloggor):
        self.logger = logger
        self.config = config
        self.connections = {}
        self.local_websocket_port = self.config["handler_port"]

        self.dank_info = DankInfoLive()

        self.boot()

    def boot(self):
        self.logger.log("DEBUG", "Boot Sequence", msg="Booting up the Handler.", file="Handler")
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(("localhost", self.local_websocket_port))
        self.logger.log("INFO", "Boot Sequence", msg=f"Fully booted up, locally serving UDP on port {self.local_websocket_port}.", file="Handler")

        self.main()

    def main(self):
        try:
            while True:
                message, addr = self.sock.recvfrom(1024)
                message = message.decode("utf-8").strip()

                self.message_handler(message, addr)
        except KeyboardInterrupt:
            self.logger.log("INFO", "Local UDP Server", msg="KeyboardInterrupt, exiting...", file="Handler")
            self.sock.close()
            raise SystemExit


    def message_handler(self, message, addr):
        message = json.loads(message.decode("UTF-8"))
        if message["op"] == 0:
            if message["data"]["valid"]:
                self.connections[message["data"]["id"]] = addr
                self.logger.log("INFO", "Local UDP Server", msg=f"Client {message['data']['id']} connected.", file="Handler")
            else:
                self.logger.log("WARNIGN", "Local UDP Server", msg=f"Token: {message['data']['token']} is invalid.", file="Handler")
        
        elif message["op"] == 1:
            self.dank_info.update(message["data"])

    def send(self, client: str, message: str) -> bool:
        if client not in self.connections.keys():
            self.logger.log("WARNING", "Local UDP Server", msg=f"Client {client} is not connected.", file="Handler")
            return False

        client_ip, client_port = self.connections[client]
        self.sock.sendto(message.encode("utf-8"), (client_ip, client_port))
        return True
