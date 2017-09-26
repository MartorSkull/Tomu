from django.db import models
from django.conf import settings
from django.utils import timezone
# Create your models here.

class Poll(models.Model):
    name = models.CharField(max_length=150)
    created = models.DateTimeField(auto_now=True)
    closetime = models.DateTimeField()
    admin = models.ForeignKey(settings.AUTH_USER_MODEL)

    def allChoices(self):
        return Choice.objects.filter(poll=self)

    def countChoices(self):
        return Choice.objects.filter(poll=self).count()

    def closed(self):
        return self.closetime<=timezone.now()

    class Meta:
        verbose_name = "poll"
        verbose_name_plural = "polls"

    def __str__(self):
        return self.name

class Choice(models.Model):
    choice = models.CharField(max_length=80)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    idinPoll = models.IntegerField()

    def voted(self):
        return Vote.objects.filter(choice=self).count()

    class Meta:
        verbose_name = "Choice"
        verbose_name_plural = "Choices"

    def __str__(self):
        return "{} @ {}".format(self.choice, self.poll.name)

class Vote(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    choice = models.ForeignKey(Choice)

    def poll(self):
        return self.choice.poll

    class Meta:
        verbose_name = "Vote"
        verbose_name_plural = "Votes"

    def __str__(self):
        return "{} @ {} @ {}".format(self.user, self.choice.choice, self.choice.poll.name)
