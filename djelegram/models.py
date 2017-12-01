from django.db import models
from django.conf import settings
# Create your models here.


class TelegramUser(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    telegram_id = models.IntegerField()
    banned = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Chatter"
        verbose_name_plural = "Chatters"

    def __str__(self):
        return self.discord_username