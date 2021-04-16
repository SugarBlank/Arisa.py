import discord
from discord.ext import commands
from discord.ext.commands import Cog
from discord.ext.commands import has_permissions


class Bot(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(brief="Sets the welcome channel to chat you talked in.")
    async def welcomelog(self, ctx):
        self.welcome_channel = ctx.message.channel
        await ctx.send(f"Welcome Channel has been set to {ctx.message.channel}.")

    @Cog.listener()
    async def on_ready(self):
        print("Bot Cog ready.")

    @commands.command(brief="Information about Arisa bot.", aliases=["botinfo"])
    async def bt(self, ctx):
        embed = discord.Embed(color=discord.Color(0xf8f8ff), description="**Arisa Bot Info:**")
        embed.set_thumbnail(url=ctx.bot.user.avatar_url)
        embed.add_field(name="Developer:", value='scouri#1078')
        embed.add_field(name="Library:", value="discord.py")
        embed.add_field(name="Discord.py Version:", value=discord.__version__)
        embed.add_field(name="Test Server Invite:", value="https://discord.gg/FMxMHEQ")
        await ctx.send(embed=embed)

    
def setup(client):
    client.add_cog(Bot(client))