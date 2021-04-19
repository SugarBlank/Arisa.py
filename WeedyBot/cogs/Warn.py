import discord
import datetime
from discord.ext import commands
from discord.ext.commands import Cog
from cogs import Database
import discord.ext.commands.errors


class Warn(commands.Cog):
    def __init__(self, client):
        self.client = client

    @Cog.listener()
    async def on_ready(self):
        Database.execute("CREATE TABLE IF NOT EXISTS userwarns (ModeratorID integer DEFAULT 0, UserID string DEFAULT '', Reasons string DEFAULT '', DateOfWarn integer DEFAULT 0, Guild string DEFAULT '')")
        print("Warn Cog ready.")

    @commands.command(pass_context=True, name="warnlimit", aliases=["warnnumber"], brief="Sets the maximum amount of warns a user can have until they get banned.")
    @commands.has_permissions(administrator=True)
    async def set_warnlimit(self, number, ctx):
        self.warnlimit = number
        await ctx.send("Warnlimit has been set to {number}.")

    @commands.command(pass_context=True, name="warn", aliases=["w"], brief="Warns a user. Use quotes around warn message for multiple words.")
    @commands.has_permissions(ban_members=True)
    async def warn(self, ctx, member: discord.Member, reason=None):
        moderator = ctx.author.display_name
        date = datetime.date.today()
        guild = ctx.message.guild
        Database.execute("INSERT into userwarns(ModeratorID, UserID, Reasons, DateOfWarn, Guild) values(?, ?, ?, ?, ?)",
                         moderator, str(member), reason, date, str(guild))
        Database.commit()
        await ctx.send(f"{member} has been warned by {ctx.author.name} for {reason}.")

    @commands.command(pass_context=True, name="warnlog", aliases=["wl"], brief="Gets all the warns a user has.", inline=False)
    async def warnlog(self, ctx, member: discord.Member = None):

        member = ctx.author if not member else member

        guild = ctx.message.guild

        rows = Database.rows("SELECT * FROM userwarns WHERE UserID = ? AND Guild = ? ORDER BY ROWID ASC",
                             str(member), str(guild))

        embed = discord.Embed(
            ctx=ctx,
            color=discord.Color(0xf8f8ff),
            timestamp=ctx.message.created_at
        )
        embed.set_thumbnail(url=member.avatar_url)

        value = '\n'.join(f'Warned on: **{row[3]}** by **{row[0]}** for:\n`{row[2]}`' for row in rows)
        embed.add_field(name=f"Warnlog for **{member}**:", value=value, inline=True)
        embed.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested by {ctx.author}")
        await ctx.send(embed=embed)

    @commands.command(pass_context=True, name="warnclear", aliases=["wc"], brief="Clears a warn from specified user.")
    @commands.has_permissions(ban_members=True)
    async def warnclear(self, ctx, member: discord.Member, reason):
        date = datetime.date.today()

        guild = ctx.message.guild

        details = Database.rows("SELECT * FROM userwarns WHERE Reasons = ? AND UserID = ? AND Guild = ?",
                                str(reason), str(member), str(guild))

        detailsprint = '\n'.join(f'Warn Reason: **{detail[2]}** \nDate Warned: **{detail[3]}** \nWarned by: \
             **{detail[0]}** \nCleared by: **{ctx.author}** on **{date}**' for detail in details)

        Database.execute("DELETE FROM userwarns WHERE Reasons = ? AND UserID = ? AND Guild = ?",
                         str(reason), str(member), str(guild))
        Database.commit()

        embed = discord.Embed(
            ctx=ctx,
            color=discord.Color(0xf8f8ff),
            timestamp=ctx.message.created_at
        )

        embed.add_field(name=f"Warn Cleaned for **{member}**:", value=detailsprint)
        embed.set_thumbnail(url=member.avatar_url)
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Warn(client))
