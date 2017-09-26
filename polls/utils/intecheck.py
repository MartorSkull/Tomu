from polls.models import *
from datetime import datetime, timedelta
from django.contrib.auth.models import AnonymousUser, User
from django.utils import timezone
from enum import IntEnum


def createResult(status, description):
    res = (status.value << 3) | description.value
    return res

def readResult(res):
    status = StatusVotes(res & 8)
    desc = Descriptions(res & 7)
    return status, desc

class StatusVotes(IntEnum):
    GOOD = 0
    BAD = 1

class Descriptions(IntEnum):
    NoError = 0
    NotLogged = 1
    Closed =  2
    ChoiceNotFound = 3
    ErrorCreatingVote = 4


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
        return createResult(StatusVotes.BAD, Descriptions.NotLogged), None
    poll = Poll.objects.filter(pk=poll_id).first()
    if not poll or poll.closetime <= timezone.now():
        return createResult(StatusVotes.BAD, Descriptions.Closed), None
    choice = Choice.objects.filter(poll=poll, idinPoll=choice_iwp).first()
    if not choice:
        return createResult(StatusVotes.BAD, Descriptions.ChoiceNotFound), None
    check = Vote.objects.filter(user=user, choice__poll=poll).first()
    if check:
        check.delete()

    vote = Vote(user=user, choice=choice)
    vote.save()

    return 0, vote