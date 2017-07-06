from django.db import models
from django.conf import settings
from django.db import models

# Create your models here.

class Chatter(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    discord_username = models.CharField(max_length=32)
    tempPassword = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Chatter"
        verbose_name_plural = "Chatters"

    def __str__(self):
        return discord_username