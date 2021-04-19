import discord
from discord.ext import commands
from discord.ext.commands import Cog
import datetime
from discord.ext.commands import has_permissions, MissingPermissions
from cogs import Database

# Logs information about users, like edited messages, deleted messages, or new


class Logger(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.channel = client.get_channel(00000000000000)

    @Cog.listener()
    async def on_ready(self):
        Database.execute("CREATE TABLE IF NOT EXISTS logchannel \
            (Guild TEXT Default '', Channel TEXT Default '', ChannelID INT Default 0)")
        print("Logger Cog ready.")

    @commands.command(brief="Sets the log channel to chat you talked in.")
    @commands.has_permissions(administrator=True)
    async def setlog(self, ctx):
        Guild = ctx.message.guild
        Channel = ctx.message.channel
        ChannelId = Channel.id
        Database.execute("DELETE FROM logchannel WHERE (Guild = ?)",
                         str(Guild))
        Database.execute("INSERT OR REPLACE INTO logchannel (Guild, Channel, ChannelID) \
            VALUES(?, ?, ?)", str(Guild), str(Channel), int(ChannelId))

        Database.commit()
        await ctx.send(f"Sending reports to {ctx.message.channel}, Doctor {ctx.author}.")

    @Cog.listener()
    async def on_message_edit(self, before, after):
        logchannel = Database.row("SELECT * FROM logchannel WHERE Guild = ?",
                                  str(before.guild))
        id = logchannel[2]
        if not after.author.bot:
            if before.content != after.content:

                embed = discord.Embed(title="Message Edited",
                                      color=0xf8f8ff,
                                      timestamp=datetime.datetime.utcnow())

                embed.set_footer(text=f"Message edited in {before.channel}")

                embed.set_author(name=f"{before.author}({before.author.id})",
                                 icon_url=before.author.avatar_url)

                fields = [("Before:", before.content, False),
                          ("After:", after.content, False)]

                for name, value, inline in fields:
                    embed.add_field(name=name, value=value, inline=inline)

                bot_channel = self.client.get_channel(id)
            await bot_channel.send(embed=embed)

    @Cog.listener()
    async def on_message_delete(self, message):
        logchannel = Database.row("SELECT * FROM logchannel WHERE Guild = ?",
                                  str(message.guild))
        id = logchannel[2]
        author = message.author

        embed = discord.Embed(color=discord.Color(0xf8f8ff),
                              timestamp=message.created_at)
        embed.add_field(name="Message Deleted in:", value=message.channel)

        embed.set_author(name=f"{author.name}({author.id})",
                         icon_url=author.avatar_url)

        embed.add_field(name="Message Content:",
                        value=message.content,
                        inline=False)

        bot_channel = self.client.get_channel(id)

        await bot_channel.send(embed=embed)

    @Cog.listener()
    async def on_member_update(self, before, after):
        logchannel = Database.row("SELECT * FROM logchannel WHERE Guild = ?",
                                  str(before.guild))
        id = logchannel[2]
        bot_channel = self.client.get_channel(id)

        if before.display_name != after.display_name:
            embed = discord.Embed(title="Member Update:",
                                  description="Nickname Change",
                                  color=0xf8f8ff,
                                  timestamp=datetime.datetime.utcnow())

            embed.add_field(name="Nickname Before:", value=before.display_name)
            embed.add_field(name="Nickname After:", value=after.display_name)
            embed.set_author(name=before)

            try:
                await bot_channel.send(embed=embed)
            except Exception:
                pass

        elif before.avatar_url != after.avatar_url:
            embed = discord.Embed(title="Member Update:",
                                  description="Avatar Change (Old to New)",
                                  color=0xf8f8ff,
                                  timestamp=datetime.datetime.utcnow())

            embed.add_field(name="Avatar Before:", value=before.avatar_url)
            embed.add_field(name="Avatar After:", value=after.avatar_url)

            try:
                await bot_channel.send(embed=embed)
            except Exception:
                pass


def setup(client):
    client.add_cog(Logger(client))
