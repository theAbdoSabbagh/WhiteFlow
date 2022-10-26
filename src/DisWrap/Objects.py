class Response:
    def __init__(self, response: list) -> None:
        self.data = response[0]
        self.format = response[1]
        self.code = int(response[2].split(" ")[0])
        self.headers = response[6]
