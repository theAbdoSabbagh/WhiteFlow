import json


def load_config():
    try:
        accounts_config = json.load(open("accounts.json"))
        base_config = json.load(open("base_config.json"))
    except:
        return False
    
    accounts = []
    for batch in accounts_config["batches"]:
        for minion in batch["minions"]:
            accounts.append(minion)
        for key, value in batch.items():
            for minion in accounts:
                if key != "minions" and key not in minion.keys():
                    minion[key] = value
    
    for key, value in base_config.items():
        for minion in accounts:
                minion[key] = value
    
    for key, value in accounts_config.items():
        if key == "batches":
            continue
        for minion in accounts:
            if key not in minion.keys():
                minion[key] = value
    
    print(accounts)

    return accounts

class DankInfoLive:
    def __init__(self):
        self.file = json.load(open("store\dankinfo.json"))


    def update(self, data) -> None:
        self.file[data["id"]] = {
            "coins": data["coins"],
            "items": data["items"]
        }
        json.dump(self.file, open("store\dankinfo.json", "w"), indent=4)
