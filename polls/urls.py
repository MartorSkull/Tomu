from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', polls, name="polls"),
    url(r'^(\d+)', poll, name="poll"),
    url(r'^getpoll/(\d+)', getPoll, name="getPoll"),
    url(r'^vote/', vote, name="vote"),
    url(r'^new/', login_required(makePoll), name="makePoll")
]

