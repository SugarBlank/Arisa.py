import random
import discord
from discord.ext import commands
from glob import glob
from pathlib import Path
from discord.ext import menus
import logging

intents = discord.Intents.all()

intents.members = True

client = commands.Bot(command_prefix='?', case_insensitive=True, intents=intents)


initial_extensions = [
    "cogs.Bot",
    "cogs.Logger",
    "cogs.Info",
    "cogs.Moderation",
    "cogs.Help",
    "cogs.Warn",
    "cogs.Scrape",
    "cogs.Chan",
    
    ]

for extension in initial_extensions:
    client.load_extension(extension)

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


@client.command(brief="Returns your ping.")
async def ping(ctx):
    await ctx.send(f":ping_pong: **{ctx.author}'s** latency is {round(client.latency * 1000)}ms!")


@client.command(aliases=['8ball', 'eightball'], brief="Obligatory 8ball command, for fun.")
async def _8ball(ctx, *, question):
    responses = ['It is certain.',
                 'Without a doubt.',
                 'You may rely on it.',
                 'Yes definitely.',
                 'It is decidedly so.',
                 'As I see it, yes.',
                 'Most likely.',
                 'Yes.',
                 'Outlook good.',
                 'Signs point to yes.',
                 'Reply hazy try again.',
                 'Better not tell you now.',
                 'Ask again later.',
                 'Cannot predict now.',
                 'Concentrate and ask again.',
                 'Don’t count on it.',
                 'Outlook not so good.',
                 'My sources say no.',
                 'Very doubtful.',
                 'My reply is no.']
    await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')

@client.command(brief="Bot spam pings, only accessible to admin, not suggested.")
@commands.has_permissions(administrator=True)
async def spam(ctx, spam="off"):
    while spam == "true":
        await ctx.send("@everyone")
        if spam == "off":
            break


@client.event
async def on_ready():
    print(f"\nLogged in as {client.user} - {client.user.id}\nDiscord Version: {discord.__version__}\n")
    await client.change_presence(activity=discord.Game('Sanitizing the Lab (?help)'))
    print("Weedy logged in and booted.")

client.run("BOT TOKEN HERE")
