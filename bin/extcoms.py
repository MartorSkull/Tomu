import discord
from discord.ext import commands
import asyncio
from dingo.utils.utils import *
from django.contrib.staticfiles.templatetags.staticfiles import static

class ExtraCommands:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def purpose(self):
        await self.bot.say("I. : {}".format("http://i.imgur.com/A6pmS0X.png"))

    @commands.command(pass_context=True, hidden=True)
    async def sendnudes(self, ctx):
        await self.bot.say("https://www.reddit.com/r/gonewild/. You're welcome {}".format(ctx.message.author.mention))

    @commands.command(pass_context=True, hidden=True)
    @anti_spam(timeBetween=datetime.timedelta(minutes=1), multiple_calls=2, until_stop_responding=2, until_blocking=3)
    async def test(self, ctx):
        await self.bot.add_reaction(ctx.message, u"\u2705")

    @commands.command()
    async def error(self):
        0/0


def setup(bot):
    bot.add_cog(ExtraCommands(bot))