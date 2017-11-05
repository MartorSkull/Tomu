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

    @commands.has_permissions(administrator=True)
    @commands.command(pass_context=True, hidden=True)
    async def announce(self, ctx, *announcement):
        string = ""
        for i in announcement:
            string+="{} ".format(i)
        await self.bot.send_message(self.bot.announcements, string)

    @commands.has_permissions(administrator=True)
    @commands.command(pass_context=True, hidden=True)
    async def bigannounce(self, ctx):
        await self.bot.send_message(ctx.message.author, "Send the announcemnt")
        message = await self.bot.wait_for_message(author=ctx.message.author)
        await self.bot.send_message(self.bot.announcements, message.content)

    @commands.command(pass_context=True)
    async def register(self, ctx):
        check = Chatter.objects.filter(discord_id=ctx.message.author.id).first()
        if check:
            await self.bot.send_message(ctx.message.author, self.bot.strings["commands"]["register"]["username_linked"])
            return
        del check
        await self.bot.send_message(ctx.message.author, self.bot.strings["commands"]["register"]["username_petition"])
        
        flag = True
        while flag:
            username = await self.bot.wait_for_message(author=ctx.message.author)
            if (isinstance(username.channel, discord.PrivateChannel)):
                flag=False

        check = Chatter.objects.filter(user__username=username.content).first()
        if check:
            await self.bot.send_message(ctx.message.author, self.bot.strings["commands"]["register"]["acc_linked_discord"])
            return
        await self.bot.send_message(ctx.message.author, self.bot.strings["commands"]["register"]["passwd"])
        
        flag = True
        while flag:
            password = await self.bot.wait_for_message(author=ctx.message.author)
            if (isinstance(username.channel, discord.PrivateChannel)):
                flag=False

        user = authenticate(username=username.content, password=password.content)
        if user:
            del username
            del password
            try:
                new = Chatter(user=user, discord_id=ctx.message.author.id, discord_username=ctx.message.author.name)
                new.save()
            except IntegrityError:
                await self.bot.send_message(ctx.message.author,self.bot.strings["commands"]["register"]["user_already_registered"] )
                return
            await self.bot.send_message(ctx.message.author, self.bot.strings["commands"]["register"]["succ_registered"] )
            return
        await self.bot.send_message(ctx.message.author, self.bot.strings["commands"]["register"]["error"])


def setup(bot):
    bot.add_cog(OfficialCommands(bot))