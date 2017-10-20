from django.contrib.auth.models import AnonymousUser, User
from discord.ext import commands
from dingo.models import Chatter
from polls.models import *
from polls.utils import intecheck
from dingo.utils.utils import *

class Polls:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    @require_login()
    @anti_spam(datetime.timedelta(minutes=5), 2)
    async def yesno(self, ctx, title: str, workhours=6):
        usr = Chatter.objects.filter(discord_id=ctx.message.author.id).first()
        poll = intecheck.create_poll(title=title, 
            workhours=workhours, 
            choices=["Yes", "No"], 
            user=usr.user)
        if isinstance(poll, Poll):
            msg = "Poll created:\n\t* To vote use this command `{1}yes {0}` or `{1}no {0}`".format(poll.id, self.bot.config['bot']['prefixes'][0])
        else:
            msg = "Please input a Title bigger than 3 characters and make sure that the closetime isn't negative"

        await self.bot.say(msg)

    @commands.command(pass_context=True)
    @require_login()
    async def yes(self, ctx, poll_id):
        usr = Chatter.objects.filter(discord_id=ctx.message.author.id).first()
        msg = await self.voteWrapp(poll_id, 0, usr, True)
        if msg:
            await self.bot.add_reaction(ctx.message, u"\u2705")

    @commands.command(pass_context=True)
    @require_login()
    async def no(self, ctx, poll_id):
        usr = Chatter.objects.filter(discord_id=ctx.message.author.id).first()
        msg = await self.voteWrapp(poll_id, 1, usr, True)
        if msg:
            await self.bot.add_reaction(ctx.message, u"\u2705")

    async def voteWrapp(self, poll_id, choice_wt_poll, chatter, yesno: bool):
        new = intecheck.vote(poll_id, choice_wt_poll, chatter.user)
        if new:
            flag = True
        else:
            flag = False
            msg = "Check the poll's id"
            if not yesno:
                msg += " and the choice's id"
            await self.bot.say(msg)
        return flag


    @commands.command(pass_context=True)
    @require_login()
    @anti_spam(datetime.timedelta(minutes=5), 2)
    async def poll(self, title, workhours=6, *choices):
        usr = Chatter.objects.filter(discord_id=ctx.message.author.id).first()
        code, poll = intecheck.create_poll(title=title, 
            workhours=workhours, 
            choices=choices, 
            user=usr.user)
        if not code:
            msg = "Poll created:\n\t* To vote use:\n"
            for i in poll.allChoices:
                msg+="\t\t* {3}vote {0} {1}: {2}\n".format(poll.id, choice.idinPoll, choice.choice, self.bot.config['bot']['prefixes'][0])
        else:
            error=[
            "Please log in",
            "The title is too small",
            "The time must be positive",
            "Please use at least 2 choices",]
            desc = intecheck.readResult(code)[1]
            if desc>=5:
                raise Exception()
            msg = error[desc]
        await self.bot.say(msg)

    @commands.command(pass_context=True)
    @require_login()
    async def vote(self, poll, choice):
        usr = Chatter.objects.filter(discord_id=ctx.message.author.id).first()
        flag = self.voteWrapp(poll, choice, usr, False)
        if flag:
            await self.bot.add_reaction(ctx.message, u"\u2705")

def setup(bot):
    bot.add_cog(Polls(bot))