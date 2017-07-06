from .models import *
from datetime import datetime, timedelta
from django.contrib.auth.models import AnonymousUser, User

def create_poll(title, workhours, choices, user):
    closetime=datetime.now() + timedelta(hours=workhours)
    if len(title)<3:
        return "NaToSh"
    elif closetime<=datetime.now():
        return False
    elif user == AnonymousUser:
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