import requests
import random
import re
import discord
from discord.ext import commands
from lxml.html import fromstring
from discord.ext.commands import Cog


API_PAGE = 'http://api.4chan.org/{}/1.json'
POST_URL_TEMPLATE = 'http://boards.4chan.org/{}/res/{}#p{}'

# Return the passed lxml.Element formatted in plain text.
# Special thanks to NotSoSuper, took most of the code here from him.
# https://github.com/NotSoSuper/NotSoBot/blob/master/mods/Chan.py


def format(element):
    formatted_element = list()
    text = [element.text, element.tail]
    if element.tag == 'br':
        text[0] = u'\n'
    text = filter(lambda x: x, text)
    text = u' '.join(text)
    formatted_element.append(text)
    for child in element:
        formatted_child = format(child)
        formatted_element.append(formatted_child)
    formatted_element = u' '.join(formatted_element)
    formatted_element = formatted_element.strip()
    formatted_element = re.sub(u' +', u' ', formatted_element)

    return formatted_element


def get_posts(board):
    # Return all posts of the board's front page.
    url = API_PAGE.format(board)
    response = requests.get(url)
    threads = response.json()
    threads = threads['threads']
    threads = map(lambda x: x['posts'], threads)
    parsed_posts = list()
    for thread in threads:
        op = thread[0]
        for post in thread:
            url = POST_URL_TEMPLATE.format(board, op['no'], post['no'])
            try:
                content = post['com']
            except KeyError:
                content = ''
            else:
                content = fromstring(content)
                content = format(content)

            parsed_posts.append({
              'content': content,
              'url': url,
            })
        return parsed_posts


def get_discord_posts(board):
    # All posts that are in discords chat limits
    posts = get_posts(board)

    posts = filter(lambda x: x['content'], posts)
    posts = filter(lambda x: len(x['content']) >= 20, posts)
    return posts


def r_f_discord_post(board):
    # Random formatted post that is within discord limits
    posts = get_discord_posts(board)
    posts = tuple(post['content'] for post in posts)
    post = random.choice(posts)
    return post


class Chan(Cog):
    def __init__(self, client):
        self.client = client

    @Cog.listener()
    async def on_ready(self):
        print("Chan Cog ready.")

    boards = ['b', 'pol', 'v', 's4s']

    @commands.group(aliases=['4chan'], invoke_without_command=True, brief="Gets random 4chan posts from boards.")
    async def chan(self, ctx, board: str is None):
        try:
            # Replies random 4chan post.
            if board is None:
                post = r_f_discord_post(random.choice(self.boards))
            else:
                post = r_f_discord_post(board.replace("/", ""))
            await ctx.send(post)
        except ValueError:
            await ctx.send("Invalid Board!")


def setup(client):
    client.add_cog(Chan(client))
