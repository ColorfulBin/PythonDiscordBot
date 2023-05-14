import discord
from discord.ext import commands
import json
import aiohttp


class horny_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.enabled = False

    @commands.command(
        name="horny_mode",
        aliases=["hmode"],
        help="Changes horny mode enabled"
    )
    async def horny_mode(self, ctx, mode):
        try:
            self.enabled = bool(mode)
        except ValueError:
            embed = discord.Embed(title="Mode Error",
                                  description="New mode does-sn't look right! :worried:",
                                  color=discord.Color.red())
            await ctx.channel.send(embed=embed, delete_after=5.0)
            await ctx.message.add_reaction("❌")

    async def ask_waifu(self, query, user_id, user_name):
        data = json.dumps({"key1": "value", "key2": "value"})
        headers = {"content-type": "application/json", "x-rapidapi-host": "waifu.p.rapidapi.com",
                   "x-rapidapi-key": "849cda582dmsh4bbee7f2347aa5bp15ae50jsnb9d45db4244c"}
        params = {"user_id": user_id, "message": query, "from_name": user_name, "to_name": "Neko DJ",
                  "situation": "We are both hella horny", "translate_from": "en", "translate_to": "en"}
        async with aiohttp.ClientSession() as session:
            async with session.post("https://waifu.p.rapidapi.com/path", data=data, headers=headers, params=params) as response:
                return await response.text(encoding='utf-8')

    @commands.Cog.listener()
    async def on_message(self, ctx):
        if ctx.author == self.bot.user or ctx.author.bot:
            return
        elif ctx.content.startswith("!>") and self.enabled:
            query = ctx.content.replace("!> ", "")
            response = await self.ask_waifu(query, ctx.author.id, ctx.author.name)
            await ctx.channel.send(response, reference=ctx)


async def setup(bot):
    await bot.add_cog(horny_cog(bot))
