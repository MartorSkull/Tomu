from django.contrib.auth.models import AnonymousUser, User
from discord.ext import commands
from dingo.models import *
import datetime
import asyncio
import functools
import json

def require_login():
    def wrapper(func):
        @functools.wraps(func)
        async def wrapped(*args, **kwargs):
            self = args[0]
            ctx = args[1]
            auth = Chatter.objects.filter(discord_id=ctx.message.author.id).first()
            if auth:
                if not auth.banned:
                    return await func(*args, **kwargs)
                else:
                    pass
            else:
                return await self.bot.send_message(ctx.message.channel, "You have to register to use some commands. Use the `{}register` command".format(self.bot.command_prefix[0]))
        return wrapped
    return wrapper


def anti_spam(timeBetween, multiple_calls=1, until_stop_responding=5, until_blocking=None):
    def wrapper(func):
        @functools.wraps(func)
        async def wrapped(*args, **kwargs):
            self = args[0]
            ctx = args[1]
            now = datetime.datetime.now()
            with open('spam', 'r+') as spam:
                reg = json.load(spam)
            dicnow={
                "year": now.year, 
                "month": now.month, 
                "day": now.day, 
                "hour": now.hour,
                "minute": now.minute,
                "second": now.second,
                "microsecond": now.microsecond}
            try:
                com = reg[ctx.message.author.id][func.__name__] 
            except KeyError as e:
                if ctx.message.author.id not in reg.keys():
                    reg[ctx.message.author.id] = {}
                reg[ctx.message.author.id][func.__name__] = {
                        "lastCall": dicnow,
                        "numberOfCalls": 0,
                        "hasBlock": False
                    }
                com = reg[ctx.message.author.id][func.__name__] 

            com["numberOfCalls"] += 1
            lastCall=datetime.datetime(**com["lastCall"])
            if now - lastCall >= timeBetween:
                com["numberOfCalls"] = 0
                com["hasBlock"] = False
                com["lastCall"] = dicnow
            elif com["numberOfCalls"] > multiple_calls:
                com["lastCall"] = dicnow

            with open("spam", 'w') as spam:
                spam.write(json.dumps(reg))

            noc = com["numberOfCalls"]

            if com["numberOfCalls"]>multiple_calls and now - datetime.datetime(**com["lastCall"])<=timeBetween:
                if not com["numberOfCalls"]-until_stop_responding>multiple_calls:
                    return await self.bot.send_message(ctx.message.channel, "Too many simultaneous calls.")
                else:
                    return

            return await func(*args, **kwargs)

        return wrapped
    return wrapper

"""
{id: {
    command: {
        lastCall: datetime, 
        numberOfCalls: int,
        hasBlock: bool
        },
        *
    },
    *
}
"""