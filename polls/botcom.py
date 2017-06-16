from django.contrib.auth.models import AnonymousUser, User
from discord.ext import commands
from datetime import datetime, timedelta
from .models import *

class Polls:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def yesno(self, ctx, title):
        poll = Poll(name=title, closetime = datetime.now() + timedelta(hours=12), admin=User.objects.all().first())
        poll.save()
        yes = Choice(poll=poll, choice="yes", idinPoll=0)
        yes.save()
        no = Choice(poll=poll, choice="no", idinPoll=1)
        no.save()

        await self.bot.say("Poll created:\n\t* To vote use this command !yes {} or !no {}".format(poll.id, poll.id))

def setup(bot):
    bot.add_cog(Polls(bot))