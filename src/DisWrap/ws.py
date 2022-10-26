from websocket import create_connection
import threading
import random
import time
import json


class Gateway:
    def __init__(self, config, logger):
        logger.log("DEBUG", "Boot Sequence", msg=f"Booting up a local discord signal client.")
        self.config = config
        self.logger = logger

        self.token = config["token"]

        self.__boot_ws()

    def heartbeat(self):
        while True:
            time.sleep(self.heartbeat_interval)
            self.ws.send_json({"op": 1, "d": None})

    def __boot_ws(self):
        self.logger.log("DEBUG", "Boot Sequence", msg="Booting up the discord websocket client.", file="DiscordSignal")
        ws = create_connection("wss://gateway.discord.gg/?v=9&encoding=json")

        hello = json.loads(ws.recv())

        self.ws = ws
        self.heartbeat_interval = hello["d"]["heartbeat_interval"]/1000
        self.logger.log("DEBUG", "Boot Sequence", msg="Booting up the discord heartbeat client.", file="DiscordSignal")

        jitter_heartbeat = self.heartbeat_interval * random.uniform(0, 0.1)

        time.sleep(jitter_heartbeat)
        ws.send(json.dumps({"op": 1, "d": None}))
        response = json.loads(ws.recv())

        if response["op"] != 11:
            self.logger.log("CRITICAL", "Boot Sequence", msg="Discord heartbeat client failed to boot.", file="DiscordSignal")
            return False

        threading.Thread(target=self.heartbeat).start()
        self.logger.log("DEBUG", "Boot Sequence", msg="Booted up the discord heartbeat client. Now IDENTIFYING", file="DiscordSignal")


        ws.send(json.dumps(
            {
                "op": 2,
                "d": {
                    "token": self.token,
                    "intents": 38408, ## Use 37377 if this doesn't work
                    "properties": {
                        "$os": "windows",
                        "$browser": "Discord",
                        "$device": "desktop"
                    }
                }
            }
        ))

        identify = ws.recv()
        if not identify:
            return "InvalidToken"

        identify_json = json.loads(identify)
        self.session_id = identify_json["d"]["session_id"]
        self.logger.log("DEBUG", "Boot Sequence", msg="READY", file="DiscordSignal")
