from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, render, redirect
from django.template import RequestContext
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import AnonymousUser
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from datetime import datetime, timedelta
from django.utils import timezone
from config.settings import BOTCONFIG
# Create your views here.

def index(request):
    return render(request, "index.html", {"prefix":BOTCONFIG["bot"]["prefixes"][0]})

def license(request):
    return render(request, "License.html")

def loginv(request):
    if request.method != "POST":
        return redirect('index')
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user != None:
        login(request, user)
    return redirect('index')

def logoutv(request):
    logout(request)
    return redirect('index')