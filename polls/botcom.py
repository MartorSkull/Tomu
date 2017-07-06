from django.contrib.auth.models import AnonymousUser, User
from discord.ext import commands
from datetime import datetime, timedelta
from .models import *
from .intecheck import *

class Polls:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def yesno(self, ctx, title: str, workhours=6):
        msgs = {
            "NaToSh": "The name for the poll has a minimum of 3 leters.",
            "WoHrNg": "The poll can't close before it started",
        }
        
        poll = create_poll(title=title, 
            workhours=workhours, 
            choices=["Yes", "No"], 
            user=User.objects.all().first())

        if poll:
            msg = "Poll created:\n\t* To vote use this command !yes {0} or !no {0}".format(poll.id)

        await self.bot.say(msg)

def setup(bot):
    bot.add_cog(Polls(bot))