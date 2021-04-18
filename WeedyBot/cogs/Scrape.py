import requests
import secrets
from discord.ext import commands
from discord.ext.commands import Cog


GEL_PAGE = 'https://gelbooru.com/index.php?page=dapi&s=post&q=index&json=1&limit=5000&tags={0}+'


def get_posts_gel(tag):
    url = GEL_PAGE.format(tag)
    search = requests.get(url).json()

    for image in search:
        randomimage = secrets.choice(search)
        imageget = randomimage.get('file_url')

    return imageget


class Scrape(commands.Cog):
    def __init__(self, client):
        self.client = client

    @Cog.listener()
    async def on_ready(self):
        print("Scrape cog is ready.")

    @commands.command(pass_context=True, name="scrape", aliases=["gel", "s"], brief="Scrapes Gelbooru for a random image. Needs to be NSFW.")
    @commands.is_nsfw()
    async def scrape(self, ctx, tag: str = None):
        try:
            image = get_posts_gel(tag)
            await ctx.send(image)
        except ValueError:
            await ctx.send(f"{tag} isn't valid, try again.")


def setup(client):
    client.add_cog(Scrape(client))
