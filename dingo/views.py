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
from config.settings import BOTCONFIG
# Create your views here.

def index(request):
    return render(request, "index.html", {"prefix":BOTCONFIG["bot"]["prefixes"][0]})

def license(request):
    return render(request, "License.html")

def register(request):
    if request.method != "POST":
         return render(request, "register.html")

    if request.method == "POST":
        print(request.POST)
        username = request.POST["username"]
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        passwd = False
        email_e = False
        usnm= False
        usnm_message = ""
        email_message = ""
        passwd_message = ""
        if password != password2:
            passwd = True
            passwd_message = "Passwords dont match"
        if (password == "") or (password2 == ""):
            passwd = True
            passwd_message = "Password's fields cant be empty"
        if username == "":
            usnm = True
            usnm_message = "Username cant be empty"
        if User.objects.filter(username=username).exists():
            usnm = True
            usnm_message = "Username is taken"
        if User.objects.filter(email=email).exists():
            email_e = True
            email_message = "Email is already in use"
        if email == "":
            email_e = True
            email_message = "Email cant be empty"
        if (usnm == False) and (email_e == False) and (passwd == False):
            user = User.objects.create_user(username, email, password)
            user.save()



    return render(request, "register.html", {"usnm": usnm,"email_e":email_e,"passwd":passwd,"usnm_message":usnm_message,"email_message": email_message,"passwd_message":passwd_message})



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