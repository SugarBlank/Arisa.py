from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions
from discord.ext.commands import Cog
from discord.ext.commands import BadArgument
import traceback

import discord

import asyncio
from discord import member


class ErrorHandler(commands.Cog):
    def __init__(self, client):
        self.client = client

    @Cog.listener()
    async def on_ready(self):
        print("ErrorHandler Cog ready.")

    @Cog.listener()
    async def on_command_error(self, ctx, error):

        if isinstance(error, MissingPermissions):
            await ctx.send(f"**{ctx.author}**, you are missing permissions!")
            pass

        elif isinstance(error, BadArgument):
            await ctx.send(f"**{ctx.author}**, you have made a bad argument.")
            return

        elif isinstance(error, commands.CommandNotFound):
            await ctx.send(f"**{ctx.author}**, this command doesn't exist!")

        elif isinstance(error, commands.UserInputError):
            await ctx.send(f"{ctx.author}, user not found!")

        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.send("Sorry I don't have permission!")

        elif isinstance(error, commands.DisabledCommand):
            await ctx.send("This command is disabled.")

        elif isinstance(error, discord.Forbidden):
            pass

        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Missing required argument!")

        elif isinstance(error, commands.MemberNotFound):
            await ctx.send("Member wasn't found!")


def setup(client):
    client.add_cog(ErrorHandler(client))