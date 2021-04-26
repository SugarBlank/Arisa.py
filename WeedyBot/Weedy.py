import random
import discord
from discord.ext import commands


intents = discord.Intents.all()

intents.members = True

client = commands.Bot(command_prefix=',',
                      case_insensitive=True,
                      intents=intents)


initial_extensions = [
    "cogs.Anime",
    "cogs.BotUtilities",
    "cogs.Chan",
    "cogs.ErrorHandler",
    "cogs.Help",
    "cogs.Info",
    "cogs.Logger",
    "cogs.Moderation",
    "cogs.Scrape",
    "cogs.Warn",
    ]

for extension in initial_extensions:
    client.load_extension(extension)


@client.command(brief="Returns Weedy's ping.")
async def ping(ctx):
    await ctx.send(f":ping_pong: **Weedy's** latency is {round(client.latency * 1000)}ms!")


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


@client.event
async def on_ready():
    print(f"\nLogged in as {client.user} - {client.user.id}\nDiscord Version: {discord.__version__}\n")
    await client.change_presence(activity=discord.Game('Sanitizing the Lab (?help)'))
    print("Weedy logged in and booted.")


client.run("BLANK")
