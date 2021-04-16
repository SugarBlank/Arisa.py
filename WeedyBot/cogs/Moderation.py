import discord
from discord.ext import commands
from discord.ext.commands import Cog, Greedy, Converter
from discord.ext.commands import MissingPermissions
import datetime
import random


class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client

    @Cog.listener()
    async def on_ready(self):
        self.log_channel = self.client.get_channel(742556488882585712)
        print("Moderation Cog ready.")

    @commands.command
    @commands.has_permissions(ban_members=True)
    async def modlogset(self):
        self.log_channel = ctx.message.channel
        await ctx.send(f"Modlog channel has been set to {ctx.message.channel}.")


    @commands.command(aliases=["b"], brief="Ban Permissions needed to ban.")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        embed = discord.Embed(color=0xf8f8ff, timestamp=ctx.message.created_at)
        embed.add_field(name="Member Banned:", value=member)
        embed.add_field(name="ID:", value=member.id)
        embed.set_thumbnail(url=member.avatar_url)
        embed.add_field(name="Ban Reason:", value=reason)
        embed.add_field(name="Banned by:", value=ctx.author.mention)

        await member.send(embed=embed)
        await member.ban(reason=reason)
        await self.log_channel(embed=embed)

    @commands.command(pass_context=True, aliases=["k"], brief="Kick permissions needed to kick.")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        embed = discord.Embed(color=discord.Color(0xf8f8ff), timestamp=ctx.message.created_at)
        embed.add_field(name="Member Kicked:", value=member)
        embed.add_field(name="ID:", value=member.id)
        embed.set_thumbnail(url=member.avatar_url)
        embed.add_field(name="Kick Reason:", value=reason)
        embed.add_field(name="Kicked by:", value=ctx.author.mention)
        await member.send(embed=embed)
        await member.kick(reason=reason)
        await self.log_channel(embed=embed)

    @commands.command(brief="Ban permissions needed. Bans member with user ID that isn't in the server.")
    @commands.has_permissions(ban_members=True)
    async def hackban(self, ctx, user: discord.Object):
        await ctx.guild.ban(discord.Object(id=user.id))
        await ctx.send("Hackbanned.")

    @commands.command(aliases=["ub"], brief="Ban permissions needed. Unbans member with user ID.")
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, member):
        member = self.client.fetch_user(int(member))
        await ctx.guild.unban(member)

        embed = discord.Embed(description=f"**{member.display_name}** has been unbanned by **{ctx.author}**.",
                              color=discord.Color(0xf8f8ff), timestamp=ctx.message.created_at)

        await self.log_channel(embed=embed)

    @commands.command(brief="Ban permissions needed. 1% chance of getting babbed too hard :sweat:.")
    @commands.has_permissions(ban_members=True)
    async def bab(self, ctx, member: discord.Member = None):
        
        roll = random.randint(1, 100)
        
        if roll == 1:
            embed = discord.Embed(color=discord.Color(0xf8f8ff), timestamp=ctx.message.created_at)
            embed.add_field(name="BABBED:", value=member)
            embed.add_field(name="ID:", value=member.id)
            embed.add_field(name="Banned for:", value="Got babbed too hard :punch: :pensive: :triumph:")

            await ctx.send(embed=embed)
            await member.send(embed=embed)

            await member.ban()

        if member == None:
            await ctx.send(f"**{ctx.author}**, you can't bab nothing SMH :angry:")


        else:
            await ctx.send(f"**{ctx.author}** successfully babbed **{member}**!")

    @commands.command(brief="Default amount of clearing is 10. Add custom integer to change the amount.")
    async def clear(self, ctx, amount=10):
        await ctx.channel.purge(limit=amount)
        await ctx.send(f"{amount} messages have been cleared.")

    @bab.error
    async def baberror(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.send(f"**{ctx.author}**, you really out here tryna BAB :rage: :rage: :rage:")

    # Role Commands




    @commands.command(aliases=["removerole"], brief="Removes role from member.")
    async def rr(self, ctx, member: discord.Member, *, role: discord.Role):
        if ctx.author.guild_permissions.administrator:
            embed = discord.Embed(color=discord.Color(0xf8f8ff),
                                  description=f"Successfully removed {role} from {member}.")
            await member.remove_roles(role)
            await ctx.send(embed=embed)

    @commands.command(pass_context=True, aliases=["giverole", "addrole"], brief="Gives member a role.")
    async def gr(self, ctx, member: discord.Member, *, role: discord.Role):
        if ctx.author.guild_permissions.administrator:
            embed = discord.Embed(color=discord.Color(0xf8f8ff), description=f"Successfully added {role} to {member}.")
            await member.add_roles(role)
            await ctx.send(embed=embed)

   
    @commands.command(brief="Returns members in a role.")
    async def inrole(self, ctx, *args):
        global member_list    
        if args == None:
            return await ctx.send("Please specify a role.")

        guild = ctx.message.guild
        role_name = (' '.join(args))
        role_id = guild.roles[0]
        member_list = []
        for role in guild.roles:
            if role_name == role.name:
                role_id = role
                break
        else:
            embed = discord.Embed(color=discord.Color(0xf8f8ff),
                                  description=f"**{ctx.author}**, role doesn't exist! Try again!")
            await ctx.send(embed=embed)
            return

        for member in guild.members:
            if role_id in member.roles:
                member_list.append(f"{member.display_name}#{member.discriminator}")

        formated_list=('\n'.join(member_list))

        embed = discord.Embed(color=0xf8f8ff)
        embed.add_field(name=f"Members in {role}:",  value=formated_list)
        await ctx.send(embed=embed)


    


        
      
      

      
#nickname commands

    @commands.command(aliases=['rename'], pass_context=True, brief="Gives a member a nickname.")
    @commands.has_permissions(kick_members=True)
    async def nick(self, ctx, member: discord.Member, nick):
        await member.edit(nick=nick)
        embed = discord.Embed(color=0xf8f8ff, description=f"{member}'s nickname has been changed to {nick}.")
        await ctx.send(embed=embed)

    @commands.command(aliases=['rn', 'removenickname'], pass_context=True, brief="Removes a member's nickname.")
    @commands.has_permissions(kick_members=True)
    async def remove_nickname(self, ctx, member: discord.Member):
        await member.edit(nick=None)
        embed = discord.Embed(color=0xf8f8ff, description=f"{member}'s nickname has been removed.")
        await ctx.send(embed=embed)

    @commands.command(aliases=['massrename', 'mrn', 'massnick'], pass_context=True, brief="Renames members with special characters.")
    @commands.has_permissions(kick_members=True)
    async def mass_nick(self, ctx, nick):
        # List full of letters with unicode and whatnot.

        guild = ctx.message.guild

        special_letters = ["ó", "ú", "ñ", "Ñ", "‡", "‡", "¿", "¬", "½", "¼", "¡", "«", "»", "¦", "ß", "µ", "±", "°",
                           "•", "·", "²", "€", "„", "…", "†", "‡", "ˆ", "‰", "Š", "‹",
                           "Œ", "‘", "’", "“", "”", "–", "—", "˜", "™", "š", "›", "œ", "Ÿ", "¨", "©", "®", "¯", "³",
                           "´", "¸", "¹", "¾", "À", "Á", "Â", "Ã", "Ä", "Å", "È",
                           "É", "Ê", "Ë", "Ì", "Í", "Î", "Ï", "Ð", "Ò", "Ó", "Ô", "Õ", "Ö", "×", "Ø", "Ù", "Ú", "Û",
                           "Ü", "Ý", "Þ", "ã", "ð", "õ", "÷", "ø", "ü", "ý", "þ",
                           "Ç", "ü", "é", "â", "ä", "à", "å", "ç", "ê", "ë", "è", "ï", "î", "ì", "æ", "Æ", "ô", "ö",
                           "ò", "û", "ù", "ÿ", "¢", "£", "¥", "P", "ƒ", "á", "í",
                           "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "<", ">", "?", "}", "{", "]", "[", "`",
                           "-", "+", "*", "/", "."]

        for member in guild.members:
            membercheck = member.display_name[0]

            if membercheck in special_letters:
                await member.edit(nick=nick)

            else:

                pass
        embed = discord.Embed(color=0xf8f8ff, description=f"Special names have been changed to {nick}.")
        await ctx.send(embed=embed)


#mute/unmute command

    @commands.command(brief="Need to have a seperate member role besides everyone for it to work.")
    @commands.bot_has_permissions(manage_roles=True)
    @commands.has_permissions(kick_members=True)
    async def mute(self, ctx, member: discord.Member):
        
        muted = discord.utils.get(member.guild.roles, name='Muted')
        roles = [role for role in member.roles]

        await member.edit(roles=[])

        await member.add_roles(muted)
        
        await ctx.send(f"**{member}** was muted by **{ctx.author}**.")


def setup(client):
    client.add_cog(Moderation(client))
