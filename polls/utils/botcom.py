from django.contrib.auth.models import AnonymousUser, User
from discord.ext import commands
from dingo.models import Chatter
from polls.models import *
from polls.intecheck import *

class Polls:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def yesno(self, ctx, title: str, workhours=6):
        usr = Chatter.objects.filter(discord_id=ctx.message.author.id).first()
        if usr:
            poll = create_poll(title=title, 
                workhours=workhours, 
                choices=["Yes", "No"], 
                user=usr.user)
            if poll:
                msg = "Poll created:\n\t* To vote use this command !yes {0} or !no {0}".format(poll.id)
            else:
                msg = "Please input a Title bigger than 3 characters and make sure that the closetime isn't negative"
        else:
            msg = "You have to register to use commands. Use the {}register command".format(self.bot.command_prefix[0])

        await self.bot.say(msg)

    @commands.command(pass_context=True)
    async def yes(self, ctx, poll_id):
        usr = Chatter.objects.filter(discord_id=ctx.message.author.id).first()
        msg = self.voteWrapp(poll_id, 0, usr, True)
        await self.bot.say(msg)

    @commands.command(pass_context=True)
    async def no(self, ctx, poll_id):
        usr = Chatter.objects.filter(discord_id=ctx.message.author.id).first()
        msg = self.voteWrapp(poll_id, 1, usr, True)
        await self.bot.say(msg)

    def voteWrapp(self, poll_id, choice_wt_poll, chatter, yesno: bool):
        if chatter:
            new = vote(poll_id, choice_wt_poll, chatter.user)
            if new:
                msg = "Saved {}".format(new.choice.choice)
            else:
                msg = "Check the poll's id"
                if not yesno:
                    msg += " and the choice's id"
        else:
            msg = "You have to register to use commands. Use the {}register command".format(self.bot.command_prefix[0])

        return msg


def setup(bot):
    bot.add_cog(Polls(bot))