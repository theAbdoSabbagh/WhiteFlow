from Modules.minion import Minion
from internals import load_config
from pyloggor import pyloggor
import os

logger = pyloggor(fn="master_log.txt")

accounts_path = os.path.join(os.getcwd(), "accounts.json")
config = load_config(accounts_path)

if not config:
    logger.log("CRITICAL", "Boot Sequence", "run.py:ValidateConfig", "Invalid config, get the latest from https://github.com/Sxvxgee/Headless")
    raise SystemExit
