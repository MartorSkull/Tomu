from django.contrib.auth.models import AnonymousUser, User
from discord.ext import commands
from dingo.models import Chatter
from polls.models import *
from .intecheck import *
from dingo.utils.utils import *

class Polls:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    @require_login()
    @anti_spam(datetime.timedelta(minutes=5), 2)
    async def yesno(self, ctx, title: str, workhours=6):
        usr = Chatter.objects.filter(discord_id=ctx.message.author.id).first()
        poll = create_poll(title=title, 
            workhours=workhours, 
            choices=["Yes", "No"], 
            user=usr.user)
        if poll:
            msg = "Poll created:\n\t* To vote use this command `!yes {0}` or `!no {0}`".format(poll.id)
        else:
            msg = "Please input a Title bigger than 3 characters and make sure that the closetime isn't negative"

        await self.bot.say(msg)

    @commands.command(pass_context=True)
    @require_login()
    async def yes(self, ctx, poll_id):
        usr = Chatter.objects.filter(discord_id=ctx.message.author.id).first()
        msg = self.voteWrapp(poll_id, 0, usr, True)
        if msg:
            await self.bot.add_reaction(ctx.message, u"\u2705")

    @commands.command(pass_context=True)
    @require_login()
    async def no(self, ctx, poll_id):
        usr = Chatter.objects.filter(discord_id=ctx.message.author.id).first()
        msg = self.voteWrapp(poll_id, 1, usr, True)
        if msg:
            await self.bot.add_reaction(ctx.message, u"\u2705")

    async def voteWrapp(self, poll_id, choice_wt_poll, chatter, yesno: bool):
        new = vote(poll_id, choice_wt_poll, chatter.user)
        if new:
            flag = True
        else:
            flag = False
            msg = "Check the poll's id"
            if not yesno:
                msg += " and the choice's id"
            await self.bot.say(msg)

        return flag


def setup(bot):
    bot.add_cog(Polls(bot))