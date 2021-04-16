import discord
from discord.ext import commands
from discord.ext.commands import Cog
import datetime
from discord.ext.commands import has_permissions, MissingPermissions
import json


# Logs information about users, like edited messages, deleted messages, or new people that have joined the server

class Logger(commands.Cog):
    def __init__(self, client):
        self.log_channel = client.get_channel(758505584676044820)
        self.client = client

    @Cog.listener()
    async def on_ready(self):
        print("Logger Cog has loaded.")


    @commands.command(brief="Sets the log channel to chat you talked in.")
    async def setlog(self, ctx):
        self.log_channel = ctx.message.channel
        await ctx.send(f"Log channel has been set to {ctx.message.channel}.")

    @Cog.listener()
    async def on_message_edit(self, before, after):

        if not after.author.bot:
            if before.content != after.content:

                embed = discord.Embed(title="Message Edited", color=0xf8f8ff, timestamp=datetime.datetime.utcnow())

                embed.set_footer(text=f"Message edited in {before.channel}")

                embed.set_author(name=f"{before.author}({before.author.id})", icon_url=before.author.avatar_url)

                fields = [("Before:", before.content, False),
                          ("After:", after.content, False)]

                for name, value, inline in fields:
                    embed.add_field(name=name, value=value, inline=inline)

                await self.log_channel.send(embed=embed)

    @Cog.listener()
    async def on_message_delete(self, message):
        author = message.author

        embed = discord.Embed(color=discord.Color(0xf8f8ff), timestamp=message.created_at)
        embed.add_field(name="Message Deleted in:", value=message.channel)
        embed.set_author(name=f"{author.name}({author.id})", icon_url=author.avatar_url)
        embed.add_field(name="Message Content:", value=message.content, inline=False)

        await self.log_channel.send(embed=embed)

    @Cog.listener()
    async def on_member_update(self, before, after):
        if before.display_name != after.display_name:
            embed = discord.Embed(title="Member Update:", description="Nickname Change:", color=0xf8f8ff,
                                  timestamp=datetime.datetime.utcnow())
            embed.add_field(name="Nickname Before:", value=before.display_name)
            embed.add_field(name="Nickname After:", value=after.display_name)
            embed.set_author(name=f"{before.author}")
            await self.log_channel.send(embed=embed)

        elif before.avatar_url != after.avatar_url:
            embed = discord.Embed(title="Member Update:", description="Avatar Change: (Old to New)", color=0xf8f8ff,
                                  timestamp=datetime.datetime.utcnow())
            embed.add_field(name="Avatar Before:", value=before.avatar_url)
            embed.add_field(name="Avatar After:", value=after.avatar_url)

            await self.log_channel.send(embed=embed)


def setup(client):
    client.add_cog(Logger(client))
