from django.apps import AppConfig
import threading

class DjelegramConfig(AppConfig):
    name = 'djelegram'

    def ready(self):
        from .bot import DjelegramB
        def djelegramThread():
            tomu = DjelegramB("443455131:AAEw-iQYha6d1DpI2IeBFjWZwi7H8ciwUZM",{})

        t = threading.Thread(target=djelegramThread, name="djelegramThread")
        t.daemon=True
        t.start()
