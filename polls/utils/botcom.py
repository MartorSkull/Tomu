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
        code, poll = intecheck.create_poll(title=title, 
            workhours=workhours, 
            choices=["Yes", "No"], 
            user=usr.user)
        if isinstance(poll, Poll):
            msg = "Poll created:\n\t* To vote use this command `{1}yes {0}` or `{1}no {0}`".format(poll.id, self.bot.config['bot']['prefixes'][0])
        else:
            msg = "Please input a Title bigger than 3 characters and make sure that the closetime isn't negative"
        await self.bot.log("{user} created a yesno poll id={id}".format(user=ctx.message.author.name, id=poll.id))
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
        code, new = intecheck.vote(poll_id, choice_wt_poll, chatter.user)
        if not code:
            flag = True
        else:
            flag = False
            error=["no",
            "Please log in",
            "This poll is closed or doens't exist",
            "Error in the choice's or the poll's id",]
            desc = intecheck.readResult(code)[1]
            if desc>=4:
                raise Exception()
            msg = error[desc]
            await self.bot.say(msg)
        return flag


    @commands.command(pass_context=True)
    @require_login()
    @anti_spam(datetime.timedelta(minutes=5), 2)
    async def poll(self, ctx, title, workhours=6, *choices):
        usr = Chatter.objects.filter(discord_id=ctx.message.author.id).first()
        code, poll = intecheck.create_poll(
            title=title, 
            workhours=workhours, 
            choices=choices, 
            user=usr.user)
        if not code:
            msg = "Poll created:\n\t* To vote use:\n"
            for choice in poll.allChoices():
                msg+="\t\t* {3}vote {0} {1}: {2}\n".format(poll.id, choice.idinPoll, choice.choice, self.bot.config['bot']['prefixes'][0])
        else:
            error=["no",
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
    async def vote(self, ctx, poll, choice):
        usr = Chatter.objects.filter(discord_id=ctx.message.author.id).first()
        flag = await self.voteWrapp(poll, choice, usr, False)
        if flag:
            await self.bot.add_reaction(ctx.message, u"\u2705")

    @commands.command(pass_context=True)
    @anti_spam(datetime.timedelta(minutes=2), 3)
    async def results(self, ctx, poll):
        try:
            poll = Poll.objects.get(id=poll)
        except django.core.exceptions.ObjectDoesNotExist:
            await self.bot.say("No poll with that id")
            return
        base = "The results for {} are: \n"
        line = "\t* {name}: {votes}({per}%)\n"
        msg = base.format(poll.name)
        for i in poll.orderedChoices():
            try:
                pers = (i.voted()*100)/poll.countVotes()
            except ZeroDivisionError:
                pers = 0
            msg+=line.format(name=i.choice, votes=i.voted(), per=pers)
        await self.bot.say(msg)

def setup(bot):
    bot.add_cog(Polls(bot))