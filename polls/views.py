from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, render, redirect
from django.template import RequestContext
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import AnonymousUser, User
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from datetime import datetime, timedelta
from django.utils import timezone
from django.core import serializers
from .models import *
from .utils import intecheck
import datetime
import re
import json
# Create your views here.

def polls(request):
    polls=Poll.objects.all().order_by("-created")
    return render(request, "polls.html", {"polls": polls})

def poll(request, id):
    try:
        poll = Poll.objects.get(pk=id)
    except Exception:
        return redirect('polls')
    return render(request, "poll.html", {"poll": poll})

def getPoll(request, id):
    poll = Poll.objects.filter(id=id).first()
    data = {
        "id": poll.id,
        "columns": [[x.choice, x.voted()] for x in poll.allChoices()],
        "code": 0,
    }

    return HttpResponse(json.dumps(data), content_type='application/json')

def makePoll(request):
    if request.method == 'POST':
        print(request.POST)
        title = request.POST['Title']
        workhours = request.POST['hours']
        answers = []
        answers = request.POST.getlist('choices[]'):

        poll = intecheck.create_poll(title=title, workhours=workhours, choices=answers, user=request.user)

        data = {"code": 1}

        return HttpResponse(json.dumps(data), content_type='application/json')

    return redirect("polls")

def vote(request):
    if request.method == 'POST':
        try:
            choice=Choice.objects.get(id=request.POST['choice'])
            poll = choice.poll
        except:
            return HttpResponse(404)
        code, voto = intecheck.vote(poll.id, choice.idinPoll, request.user)
        if code == 0:
            return getPoll(request, poll.id)
        else:
            data = {"code": code}
            return HttpResponse(json.dumps(data), content_type='application/json')
