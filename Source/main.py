from rich import print
from toml import loads
from DankCord import Config
from pyloggor import pyloggor

from internal.objects import Settings
from internal.botbase import Bot

with open("config.toml", "r+", encoding="utf-8") as f:
    settings = Settings(loads(f.read()))

bot = Bot(
    Config(
        settings.credentials.token,
        settings.credentials.channel_id
    ),
    pyloggor(
        show_file=False,
        show_topic=False,
        show_symbol=False,
        show_time=False,
        title_level=True,
        level_adjustment_space=0,
    ),
)

bot.start_autofarming()