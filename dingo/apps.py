from django.apps import AppConfig
from .bot.bot import DingoB
import threading
import asyncio

class DingoConfig(AppConfig):
    name = 'dingo'

    def ready(self):
        t = threading.Thread(target=botThread, name="botthread")
        t.daemon=True
        t.start()

def botThread():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    bot = DingoB()
    bot.begin()