from polls.models import *
from datetime import datetime, timedelta
from django.contrib.auth.models import AnonymousUser, User
from django.utils import timezone


def create_poll(title, workhours, choices, user):
    closetime=datetime.now() + timedelta(hours=workhours)
    if len(title)<3 or closetime<=datetime.now() or isinstance(user, AnonymousUser):
        return False

    poll = Poll(name=title, 
        closetime = closetime, 
        admin=user)
    poll.save()

    for i in range(len(choices)):
        choice = Choice(choice=choices[i], 
            poll=poll, 
            idinPoll=i)
        choice.save()

    return poll

def vote(poll_id, choice_iwp, user):
    if isinstance(user, AnonymousUser):
        return False
    poll = Poll.objects.filter(pk=poll_id).first()
    if not poll or poll.closetime <= timezone.now():
        return False
    choice = Choice.objects.filter(poll=poll, idinPoll=choice_iwp).first()
    if not choice:
        return False
    check = Vote.objects.filter(user=user, choice__poll=poll).first()
    if check:
        check.delete()

    vote = Vote(user=user, choice=choice)
    print(vote)
    vote.save()

    return vote