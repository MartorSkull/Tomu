from django.contrib.auth.models import AnonymousUser, User
from discord.ext import commands
from datetime import datetime, timedelta
from dingo.models import Chatter
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

        usr = Chatter.objects.filter(discord_id=ctx.message.author.id).first()
        print(usr)
        if usr:
            poll = create_poll(title=title, 
                workhours=workhours, 
                choices=["Yes", "No"], 
                user=usr.user)
            if poll:
                msg = "Poll created:\n\t* To vote use this command !yes {0} or !no {0}".format(poll.id)
        else:
            msg = "You have to register to use commands. Use the {}register command".format(self.bot.command_prefix[0])

        await self.bot.say(msg)



def setup(bot):
    bot.add_cog(Polls(bot))