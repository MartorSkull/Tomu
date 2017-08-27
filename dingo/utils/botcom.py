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
        await self.bot.say("hi {}, how are you?".format(ctx.message.author.mention))

    @commands.command(pass_context=True)
    async def register(self, ctx):
        check = Chatter.objects.filter(discord_id=ctx.message.author.id).first()
        if check:
            await self.bot.send_message(ctx.message.author, "This discord account has already a username linked to it")
            return
        del check
        counter = 0
        await self.bot.send_message(ctx.message.author, "Please send a message with your username in the website")
        username = await self.bot.wait_for_message(author=ctx.message.author)
        check = Chatter.objects.filter(user__username=username.content).first()
        if check:
            await self.bot.send_message(ctx.message.author, "This account has already been linked to another discord account")
            return
        await self.bot.send_message(ctx.message.author, "Please send the password.")
        password = await self.bot.wait_for_message(author=ctx.message.author)
        user = authenticate(username=username.content, password=password.content)
        if user:
            del username
            del password
            try:
                new = Chatter(user=user, discord_id=ctx.message.author.id, discord_username=ctx.message.author.name)
                new.save()
            except IntegrityError:
                await self.bot.send_message(ctx.message.author, "You are already registered. you don't have to use this command again")
                return
            await self.bot.send_message(ctx.message.author, "Success now you can use the commands in the server. Also you can delete the message with your password. It will not be saved")
            return
        await self.bot.send_message(ctx.message.author, "That wasn't quite right. Try again")


def setup(bot):
    bot.add_cog(OfficialCommands(bot))