from django.apps import AppConfig
from .bot.config import BotConfiguration
from .bot.bot import TomuB
from django.conf import settings
import threading
import asyncio

class TomuConfig(AppConfig):
    name = 'tomu'


def ready():
    t = threading.Thread(target=botThread, name="botthread")
    t.start()

def botThread():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    config = BotConfiguration()
    bot = TomuB(config.config, settings)
    bot.start()