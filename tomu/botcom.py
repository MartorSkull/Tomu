import discord
from discord.ext import commands


class testCommands:
    def __init__(self, bot):
        self.bot = bot


    @commands.command(pass_context=True)
    async def hi(self, ctx):
        await self.bot.say("hi {}, how are you?".format(ctx.message.author.name))

    @commands.command(pass_context=True)
    async def sendnudes(self, ctx):
        await self.bot.say("https://www.reddit.com/r/gonewild/. You're welcome {}".format(ctx.message.author.name))

def setup(bot):
    bot.add_cog(testCommands(bot))