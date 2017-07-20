from django.apps import AppConfig
import threading
import asyncio

class DingoConfig(AppConfig):
    name = 'dingo'

    def ready(self):
        from .bot import DingoB
        def botThread():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            bot = DingoB()
            bot.begin()

        t = threading.Thread(target=botThread, name="BotsThread")
        t.daemon=True
        t.start()
