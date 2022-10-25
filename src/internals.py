import json


def load_config(fn):
    try:
        config = json.load(open(fn))
    except:
        return False

    return config