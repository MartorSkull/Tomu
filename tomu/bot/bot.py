#!/usr/bin/python3.5
# -*- coding: utf-8 -*-
from discord.ext import commands
from django.conf import settings
import discord
import asyncio
import os
import traceback
import importlib

class TomuB:
    def __init__(self, config, settings):
        self.config=config

        prefix=config['bot']['prefixes']
        description = config["strings"]["description"]

        bot = commands.Bot(command_prefix=prefix, description=description, pm_help=None)

        self.bot=bot

        self.bot.announcements=config['server']['announces'].lower()
        self.bot.output =  config['server']['output'].lower()

        self.bot.botrole = config['server']['bot-role']
        self.bot.adminrole = config['server']['admin-role']
        self.botcolor = discord.Colour(config['server']['bot-color'])
        self.admincolor = discord.Colour(config['server']['admin-color'])

        self.commodule = config['main']['botmodule']

        #took this from Kurisu
        @bot.event
        async def on_command_error(error, context):
            if isinstance(error, discord.ext.commands.errors.CommandNotFound):
                pass 
            if isinstance(error, discord.ext.commands.errors.CheckFailure):
                await self.bot.send_message(context.message.channel, "{} Yossion to use this command.".format(context.message.author.mention))
            elif isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
                formatter = commands.formatter.HelpFormatter()
                await self.bot.send_message(context.message.channel, "{} You are missing required arguments.\n{}".format(context.message.author.mention, formatter.format_help_for(context, context.command)[0]))
            else:
                if context.command:
                    await self.bot.send_message(context.message.channel, "An error occured while processing the `{}` command.".format(context.command.name))
                    print('Ignoring exception in command {}'.format(context.command))
                    traceback.print_exception(type(error), error, error.__traceback__)

        @bot.event
        async def on_ready():
            if self.bot.all_ready:
                return
            #print self.bot info
            print("-------")
            print("Logged: "+ str(self.bot.is_logged_in))
            print("UserName: "+self.bot.user.name)
            print("Description: "+ self.bot.description)
            print("ID: "+ self.bot.user.id)
            print("-------")

            #get the working server. This self.bot would work better with only one server
            for server in self.bot.servers:
                self.bot.server = server

            self.myself = discord.utils.get(server.members, name=self.bot.user.name)

            #create the defult roles
            br = discord.utils.get(self.myself.roles, name=self.bot.botrole)
            if br:
                self.bot.botrole = br
            else:
                self.bot.botrole = await self.bot.create_role(server, name=self.bot.botrole, permissions=discord.Permissions().all(), colour=self.botcolor, hoist=True, mentionable=False)
                await self.bot.add_roles(self.myself, self.bot.botrole)

            ar = discord.utils.get(server.roles, name=self.bot.adminrole)
            if ar:
                self.bot.adminrole = ar
            else:
                self.bot.adminrole = await self.bot.create_role(server, name=self.bot.adminrole, permissions=discord.Permissions.all(), colour=admincolor, hoist=True, mentionable=True)

            #Default channels
                #announcements
            an=discord.utils.get(server.channels, name=self.bot.announcements)
            if not an:
                everyone_perms = discord.PermissionOverwrite(send_messages=False, send_tts_messages=False)
                my_perms = discord.PermissionOverwrite(send_messages=True, send_tts_messages=True)

                await self.bot.edit_channel_permissions(server.default_channel, server.default_role, everyone_perms)
                await self.bot.edit_channel_permissions(server.default_channel, self.bot.botrole, my_perms)
                await self.bot.edit_channel(server.default_channel, name=self.bot.announcements)

            self.bot.announcements = server.default_channel
            await self.bot.move_channel(self.bot.announcements, 0)
                #output
            op = discord.utils.get(server.channels, name=self.bot.output)
            if not op:
                everyone_perms = discord.PermissionOverwrite(read_messages=False)
                self.bot_perms = discord.PermissionOverwrite(read_messages=True)
                admin_perms = discord.PermissionOverwrite(read_messages=True)

                everyone = discord.ChannelPermissions(target=server.default_role, overwrite=everyone_perms)
                mine = discord.ChannelPermissions(target=self.bot.botrole, overwrite=self.bot_perms)
                adminperm = discord.ChannelPermissions(target=self.bot.adminrole, overwrite=admin_perms)

                op = await self.bot.create_channel(server, self.bot.output, everyone, mine, adminperm)
            self.bot.output = op
            await self.bot.move_channel(self.bot.output, 1)

            self.bot.all_ready=True

            msg=""
            if len(self.failed_addons) != 0:
                msg += "\n\nFailed to load:\n"
                for f in self.failed_addons:
                    msg += "\n{}: `{}: {}`".format(*f)
                await self.bot.send_message(self.bot.output, msg)

            await self.bot.send_message(self.bot.output, "{} is back.".format(self.bot.user.name))

        self.bot.all_ready = False

        addons=[]

        for i in settings.INSTALLED_APPS:
            check = importlib.util.find_spec(".{}".format(self.commodule), package=i)
            if check is not None:
                addons.append("{}.{}".format(i, self.commodule))

        self.failed_addons = []

        for addon in addons:
            try:
                self.bot.load_extension(addon)
            except Exception as e:
                print('Error on {}:\n {}: {}'.format(addon, type(e).__name__, e))
                self.failed_addons.append([addon, type(e).__name__, e])


    def start(self):
        self.bot.run(self.config['main']['token'])