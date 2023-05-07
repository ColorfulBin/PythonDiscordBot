import discord
from discord.ext import commands
from jokeapi import Jokes
import random
import os


class general_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.moderated_words = []
        directory = os.getcwd()
        with open(fr"{directory}\general\moderated_words.txt", "r") as mw:
            words = mw.readlines()
            for word in words:
                self.moderated_words.append(word.split("\n")[0])

    @commands.Cog.listener()
    async def on_message(self, ctx):
        for mute_word in self.moderated_words:
            if mute_word in ctx.content.lower().split(" "):
                await ctx.delete()
                mute_word_embed = discord.Embed(title="Message Moderated",
                                                description=f"**{ctx.author.mention}**, pl-lease do not use b-bad words! :confounded:",
                                                color=discord.Color.dark_orange())
                await ctx.channel.send(embed=mute_word_embed, delete_after=5.0)

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        if member.guild.system_channel:
            await member.guild.system_channel.send(f"`{member.name} has joined our family` :partying_face:")

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        if member.guild.system_channel:
            await member.guild.system_channel.send(f"`{member.name} has left our family` :sob:")

    @commands.command()
    async def roll(self, ctx, dice):
        try:
            dice = int(dice)
            await ctx.channel.send(f"Hmm, I'll choose **{str(random.randint(1, dice))}**! Wish I could help you! :smile:")
        except ValueError:
            await ctx.channel.send(f"W-wait, **{dice}** isn't look-king like the real dic-ce! :confused:")

    @commands.command()
    async def choose(self, ctx, *choices):
        if not choices:
            await ctx.channel.send("W-wait, where ar-re the options?! :cry:")
        elif len(choices) == 1:
            await ctx.channel.send("B-but it's only on-ne option here... :cry:")
        else:
            await ctx.channel.send(f"I'll choose **{str(random.choice(choices))}**! Wish I could help you :smile:")

    @commands.command()
    async def joined(self, ctx, member: discord.Member):
        await ctx.channel.send(f"{member.name} joined {discord.utils.format_dt(member.joined_at)} :smile:")

    @commands.command()
    async def ping(self, ctx):
        await ctx.channel.send(f"{int(self.bot.latency*1000)} ms! Wish I could help you :smile:")

    @commands.command()
    async def joke(self, ctx):
        j = await Jokes()
        blacklist = ["racist"]
        if not ctx.message.channel.is_nsfw():
            blacklist.append("nsfw")
        joke = await j.get_joke(blacklist=blacklist)
        if joke["type"] == "single":
            await ctx.channel.send(joke["joke"])
        else:
            await ctx.channel.send(str(joke["setup"] + f' ||{joke["delivery"]}||'))

    @commands.command()
    async def ban(self, ctx, member: discord.Member, reason: str):
        if ctx.author.guild_permissions.ban_members:
            await member.ban(reason=reason)
            embed = discord.Embed(title="User Banned!",
                                  description=f"**{member}** was ban-ned...",
                                  color=discord.Color.green())
            await ctx.send(embed=embed, delete_after=5.0)
        else:
            embed = discord.Embed(title="Permission Denied",
                                  description="You do-on't have permis-ssion to use this comma-and!",
                                  color=discord.Color.red())
            await ctx.send(embed=embed, delete_after=5.0)
            await ctx.message.add_reaction("❌")

    @commands.command()
    async def mute(self, ctx, member: discord.Member):
        is_member_muted = False
        for role in member.roles:
            if role.name == "Muted":
                is_member_muted = True
        if ctx.author.guild_permissions.manage_roles and not is_member_muted:
            await member.add_roles(discord.utils.get(member.guild.roles, name='Muted'))
            embed = discord.Embed(title="User Muted!",
                                  description=f"**{member.name}** was mut-ted...",
                                  color=discord.Color.green())
            await ctx.send(embed=embed, delete_after=5.0)
        elif is_member_muted:
            embed = discord.Embed(title="Role Error",
                                  description="Looks like t-this user is mut-ted already!",
                                  color=discord.Color.red())
            await ctx.send(embed=embed, delete_after=5.0)
            await ctx.message.add_reaction("❌")
        else:
            embed = discord.Embed(title="Permission Denied",
                                  description="You do-on't have permis-ssion to use this comma-and!",
                                  color=discord.Color.red())
            await ctx.send(embed=embed, delete_after=5.0)
            await ctx.message.add_reaction("❌")

    @commands.command()
    async def unmute(self, ctx, member: discord.Member):
        is_member_muted = False
        for role in member.roles:
            if role.name == "Muted":
                is_member_muted = True
        if ctx.author.guild_permissions.manage_roles and is_member_muted:
            role = discord.utils.get(member.guild.roles, name="Muted")
            await member.remove_roles(role)
            embed = discord.Embed(title="User Unmuted!",
                                  description=f"**{member.name}** was unmuted! :smile:",
                                  color=discord.Color.green())
            await ctx.send(embed=embed, delete_after=5.0)
        elif not is_member_muted:
            embed = discord.Embed(title="Role Error",
                                  description="Looks like t-this user isn't mut-ted!",
                                  color=discord.Color.red())
            await ctx.send(embed=embed, delete_after=5.0)
            await ctx.message.add_reaction("❌")
        else:
            embed = discord.Embed(title="Permission Denied",
                                  description="You do-on't have permis-ssion to use this comma-and!",
                                  color=discord.Color.red())
            await ctx.send(embed=embed, delete_after=5.0)
            await ctx.message.add_reaction("❌")


async def setup(bot):
    for guild in bot.guilds:
        is_muted_exist = False
        for role in await guild.fetch_roles():
            if role.name == "Muted":
                is_muted_exist = True
        if not is_muted_exist:
            role = await guild.create_role(name="Muted",
                                           color=discord.Color.red(),
                                           hoist=True,
                                           permissions=discord.Permissions(send_messages=False))
            for channel in guild.text_channels:
                await channel.set_permissions(role, send_messages=False)
    await bot.add_cog(general_cog(bot))
