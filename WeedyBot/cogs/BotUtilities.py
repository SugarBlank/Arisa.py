import discord
from discord.ext import commands
from discord.ext.commands import Cog
import psutil
import platform
import distro
import time


def uptime():
    return round((time.time() - psutil.boot_time()) / 60, 2)


class BotUtilities(commands.Cog):
    def __init__(self, client):
        self.client = client

    @Cog.listener()
    async def on_ready(self):
        print("BotUtilities Cog ready.")

    @commands.command(brief="Information about the Weedy bot.", aliases=["botinfo"], inline=True)
    async def bt(self, ctx):
        embed = discord.Embed(color=discord.Color(0xf8f8ff), description="**Weedy Bot Info:**")
        embed.set_thumbnail(url=ctx.bot.user.avatar_url)
        embed.add_field(name="Developer:", value='scouri#1078')
        embed.add_field(name="Library:", value="discord.py")
        embed.add_field(name="Discord.py Version:", value=discord.__version__)
        embed.add_field(name="Test Server Invite:", value="https://discord.gg/FMxMHEQ")
        await ctx.send(embed=embed)

    @commands.command(brief="Weedy's status", aliases=["st", "status"])
    async def weedystatus(self, ctx):
        memoryused = round(psutil.virtual_memory().used / 1000000000, 2)
        memory = f"{memoryused}GB"

        embed = discord.Embed(color=discord.Color(0xf8f8ff), description="**Weedy's Status:**", inline=True)
        embed.add_field(name="Python Version:", value=platform.python_version())
        embed.add_field(name="Discord.py Version:", value=discord.__version__)
        embed.add_field(name="Operating System:", value=distro.id())
        embed.add_field(name="Kernel Version:", value=platform.platform())
        embed.add_field(name="RAM Usage:", value=memory)
        embed.add_field(name="Uptime:", value=f"{uptime()} minutes.")
        embed.set_thumbnail(url=ctx.bot.user.avatar_url)
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(BotUtilities(client))
