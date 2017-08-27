import discord
from discord.ext import commands
import asyncio
from dingo.utils.utils import *

class ExtraCommands:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def purpose(self):
        await self.bot.say("I. Pass. Butter")

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