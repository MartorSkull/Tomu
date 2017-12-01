#!/usr/bin/python3
# -*- coding: utf-8 -*-
from django.conf import settings
from djelegram.models import *
from django.contrib.auth.models import User
from telegram.ext import Updater, CommandHandler
import telegram
import os
import traceback
import importlib
import atexit
from datetime import datetime
import logging

class DjelegramB:
    def __init__(self, token, config): 
        self.plugins = []
        self.logger = logging.getLogger(__name__)
        
        self.updater = Updater(token=token)
        self.dispatcher = self.updater.dispatcher
        start_handler = CommandHandler('start', self.start)
        self.dispatcher.add_handler(start_handler)
        self.updater.start_polling()

    #def add_plugin(self, pluginInst):

    def start(self,bot,update):
        bot.sendMessage(chat_id=update.message.chat_id, text="Hi im Mr. Tomu look at me!!!!")

