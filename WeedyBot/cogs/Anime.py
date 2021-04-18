import nekos
import discord
from discord.ext import commands
from discord.ext.commands import Cog


class Anime(commands.Cog):
    def __init__(self, client):
        self.client = client

    @Cog.listener()
    @commands.has_permissions(ban_members=True)
    async def on_ready(self):
        print("Moderation Cog ready.")

    @commands.command(brief="Sends cat pictures!")
    async def cat(self, ctx):
        await ctx.send(nekos.cat())

    @commands.command(brief="Kiss someone, even yourself :flushed:")
    async def kiss(self, ctx, member: discord.Member = None):
        if member is None:
            embed = discord.Embed(color=discord.Color(0xf8f8ff), description="lol you kissed youself!")
            embed.set_image(url=nekos.img("kiss"))
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(color=discord.Color(0xf8f8ff), description=f"{ctx.author} kissed {member}!")
            embed.set_image(url=nekos.img("kiss"))
            await ctx.send(embed=embed)

    @commands.command(brief="Send cute catgirl pictures uwu")
    async def catgirl(self, ctx):
        embed = discord.Embed(color=discord.Color(0xf8f8ff), description="have some cute catgirls owo")
        embed.set_image(url=nekos.img("neko"))
        await ctx.send(embed=embed)

    @commands.command(brief="Physical abuse never good :pensive:")
    async def slap(self, ctx, member: discord.Member = None):
        if member is None:
            embed = discord.Embed(color=discord.Color(0xf8f8ff), description="stop slapping youself!")
            embed.set_image(url=nekos.img("slap"))
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(color=discord.Color(0xf8f8ff), description=f"{ctx.author} slapped {member}! Get owned :punch: :triumph:")
            embed.set_image(url=nekos.img("slap"))
            await ctx.send(embed=embed)

    @commands.command(brief="Questionable backgrounds, requires NSFW channel.")
    @commands.is_nsfw()
    async def background(self, ctx, member: discord.Member = None):
        embed = discord.Embed(color=discord.Color(0xf8f8ff), description="nice wallpaper bro")
        embed.set_image(url=nekos.img("wallpaper"))
        await ctx.send(embed=embed)

    @commands.command(brief="Cuddle with someone :flushed:")
    async def cuddle(self, ctx, member: discord.Member = None):
        if member is None:
            embed = discord.Embed(color=discord.Color(0xf8f8ff), description="life must suck if you're cuddling youself :pensive:")
            embed.set_image(url=nekos.img("cuddle"))
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(color=discord.Color(0xf8f8ff), description=f"{ctx.author} cuddled {member} :flushed:")
            embed.set_image(url=nekos.img("cuddle"))
            await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Anime(client))
