from discord.ext import commands
from discord.ext.commands import MissingPermissions
from discord.ext.commands import Cog
from discord.ext.commands import BadArgument
from discord.ext.commands.errors import NSFWChannelRequired
import discord


class ErrorHandler(commands.Cog):
    def __init__(self, client):
        self.client = client

    @Cog.listener()
    async def on_ready(self):
        print("ErrorHandler Cog ready.")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):

        if isinstance(error, MissingPermissions):
            await ctx.send(f"**{ctx.author}**, you are missing permissions!")
            pass

        elif isinstance(error, BadArgument):
            await ctx.send(f"**{ctx.author}**, you have made a bad argument.")
            return

        elif isinstance(error, commands.CommandNotFound):
            await ctx.send(f"**{ctx.author}**, this command doesn't exist!")
            return

        elif isinstance(error, commands.UserInputError):
            await ctx.send(f"{ctx.author}, user not found!")
            return
        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.send("Sorry I don't have permission!")
            return
        elif isinstance(error, commands.DisabledCommand):
            await ctx.send("This command is disabled.")
            return
        elif isinstance(error, discord.Forbidden):
            pass

        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Missing required argument!")

        elif isinstance(error, commands.MemberNotFound):
            embed = discord.Embed(color=discord.Color(0xf8f8ff), description="No user found with that name.")
            await ctx.send(embed)
            return

        elif isinstance(error, NSFWChannelRequired):
            await ctx.send("You need to be in a NSFW channel!")
            pass


def setup(client):
    client.add_cog(ErrorHandler(client))
