from django.conf.urls import url
from .views import *
from tomu import apps

urlpatterns = [
    url(r'^$', polls, name="polls"),
    url(r'^getpoll/(\d+)', getPoll, name="getPoll"),
#    url(r'^vote/(\d)', vote, name="vote"),
    url(r'^new/', login_required(makePoll) , name="makePoll")
]

apps.ready()