from polls.models import *
from datetime import datetime, timedelta
from django.contrib.auth.models import AnonymousUser, User
from django.utils import timezone
from enum import IntEnum


def createResult(status, description):
    res = (status.value << 3) | description.value
    return res

def readResult(res):
    status = Status(res & 8 >> 3)
    desc = DescriptionsVotes(res & 7)
    return status, desc

class Status(IntEnum):
    GOOD = 0
    BAD = 1

class DescriptionsVotes(IntEnum):
    NoError = 0
    NotLogged = 1
    Closed =  2
    ChoiceNotFound = 3
    ErrorCreatingVote = 4

class DescriprionsPolls(IntEnum):
    NoError = 0
    NotLogged = 1
    SmallTitle = 2
    NegativeTime = 3
    NoChoices = 4
    ErrorCreatingPoll = 5
    ErrorCreaatingChoices = 6

def create_poll(title, workhours, choices, user):
    closetime=timezone.now() + timedelta(hours=int(workhours))
    if len(title)<3:
        return createResult(Status.BAD, DescriprionsPolls.SmallTitle), None

    if closetime<=timezone.now():
        return createResult(Status.BAD, DescriprionsPolls.NegativeTime), None

    if not user.is_authenticated:
        return createResult(Status.BAD, DescriprionsPolls.NotLogged), None

    if len(choices)<2:
        return createResult(Status.BAD, DescriprionsPolls.NoChoices), None

    try:
        poll = Poll(name=title, 
            closetime = closetime, 
            admin=user)
        poll.save()
    except:
        return createResult(Status.BAD, DescriprionsPolls.ErrorCreatingPoll), None
    try:
        for i in range(len(choices)):
            choice = Choice(choice=choices[i], 
                            poll=poll, 
                            idinPoll=i)
            choice.save()
    except:
        return createResult(Status.BAD, DescriprionsPolls.ErrorCreaatingChoices), None
        poll.delete()

    return 0, poll

def vote(poll_id, choice_iwp, user):
    if not user.is_authenticated:
        return createResult(Status.BAD, DescriptionsVotes.NotLogged), None

    poll = Poll.objects.filter(pk=poll_id).first()
    if not poll or poll.closetime <= timezone.now():
        return createResult(Status.BAD, DescriptionsVotes.Closed), None

    choice = Choice.objects.filter(poll=poll, idinPoll=choice_iwp).first()
    if not choice:
        return createResult(Status.BAD, DescriptionsVotes.ChoiceNotFound), None

    check = Vote.objects.filter(user=user, choice__poll=poll).first()
    if check:
        check.delete()

    try:
        vote = Vote(user=user, choice=choice)
        vote.save()
    except:
        return createResult(Status.BAD, DescriprionsVotes.ErrorCreatingVote), None

    return 0, vote