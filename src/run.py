from Modules.minion import Minion
from internals import load_config
from pyloggor import pyloggor
import os

logger = pyloggor(fn="master_log.txt")

try:
    accounts = load_config()
except Exception as e:
    logger.log("ERROR", "Config Loader", msg=f"Failed to load config: {e}", file="Master")
    raise SystemExit
