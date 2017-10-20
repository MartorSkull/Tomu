import discord
from django.db import IntegrityError
from discord.ext import commands
from dingo.models import Chatter
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from dingo.utils.utils import *

class OfficialCommands:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def hi(self, ctx):
        await self.bot.say(self.bot.strings["commands"]["hi"].format(**{'name':ctx.message.author.mention}))

    @commands.command(pass_context=True)
    async def register(self, ctx):
        check = Chatter.objects.filter(discord_id=ctx.message.author.id).first()
        if check:
            await self.bot.send_message(ctx.message.author, self.bot.strings["utils"]["register"]["username_linked"])
            return
        del check
        counter = 0
        await self.bot.send_message(ctx.message.author, self.bot.strings["utils"]["register"]["username_petition"])
        username = await self.bot.wait_for_message(author=ctx.message.author)
        check = Chatter.objects.filter(user__username=username.content).first()
        if check:
            await self.bot.send_message(ctx.message.author, self.bot.strings["utils"]["register"]["acc_linked_discord"])
            return
        await self.bot.send_message(ctx.message.author, self.bot.strings["utils"]["register"]["passwd"])
        password = await self.bot.wait_for_message(author=ctx.message.author)
        user = authenticate(username=username.content, password=password.content)
        if user:
            del username
            del password
            try:
                new = Chatter(user=user, discord_id=ctx.message.author.id, discord_username=ctx.message.author.name)
                new.save()
            except IntegrityError:
                await self.bot.send_message(ctx.message.author,self.bot.strings["utils"]["register"]["user_already_registered"] )
                return
            await self.bot.send_message(ctx.message.author, self.bot.strings["utils"]["register"]["succ_registered"] )
            return
        await self.bot.send_message(ctx.message.author, self.bot.strings["utils"]["register"]["error"])


def setup(bot):
    bot.add_cog(OfficialCommands(bot))