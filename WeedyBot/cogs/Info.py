import discord
from discord.ext import commands
from discord.ext.commands import Cog


class Info(commands.Cog):
    def __init__(self, client):
        self.client = client

    @Cog.listener()
    async def on_ready(self):
        print("Info Cog ready.")

    @commands.command(pass_context=True, name="userinfo", aliases=["whois"], brief="Sends information about specified user.")
    async def userinfo(self, ctx, member: discord.Member = None):
        member = ctx.author if not member else member

        roles = [role for role in member.roles]

        embed = discord.Embed(color=discord.Color(0xf8f8ff), timestamp=ctx.message.created_at)

        embed.set_author(name=f"User Info: {member}")
        
        embed.set_thumbnail(url=member.avatar_url)

        embed.add_field(name="ID", value=member.id)
        
        embed.add_field(name="Server Name", value=member.display_name)
        
        embed.add_field(name="Created at:", value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
        
        embed.add_field(name="Joined on:", value=member.joined_at.strftime('%a, %#d %B %Y, %I:%M %p UTC'))
        
        embed.add_field(name="Highest Role", value=member.top_role.mention)
        
        embed.add_field(name=f"Roles ({len(roles)})", value=" ".join(role.mention for role in roles))
        
        embed.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested by {ctx.author}")
        await ctx.send(embed=embed)

    @commands.command(brief="Sends information about the server.")
    async def server_info(self, ctx):
        
        embed = discord.Embed(color=discord.Color(0xf8f8ff), title=f'{ctx.guild.name}',
                              timestamp=ctx.message.created_at)
        
        embed.set_thumbnail(url=f'{ctx.guild.icon_url}')
        
        embed.add_field(name="Owner:", value=ctx.guild.owner)
        
        embed.add_field(name="Server ID:", value=ctx.guild.id)
        
        embed.add_field(name="Region:", value=ctx.guild.region)
        
        embed.add_field(name="Member Count:", value=ctx.guild.member_count)
        
        embed.add_field(name="Created On:", value=ctx.guild.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
        
        embed.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested by: {ctx.author}")

        await ctx.send(embed=embed)

    @commands.command(aliases=['pfp'], brief="Sends profile picture for specified member.")
    async def avatar(self, ctx, member: discord.Member = None):
        member = ctx.author if not member else member

        embed = discord.Embed(color=discord.Color(0xf8f8ff), title=f'{member}')

        embed.set_image(url=f'{member.avatar_url}')

        embed.add_field(name='Avatar', value="\n\u200b")

        await ctx.send(embed=embed)

    @commands.command(aliases=["ed"], pass_context=True, brief="Sends information about specified emote.")
    async def emote_detail(self, ctx, emote: discord.Emoji):
        embed = discord.Embed(color=0xf8f8ff, title=f"{emote.name}", timestamp=ctx.message.created_at)

        embed.set_thumbnail(url=emote.url)

        embed.add_field(name="Url:", value=emote.url)

        await ctx.send(embed=embed)

        

def setup(client):
    client.add_cog(Info(client))