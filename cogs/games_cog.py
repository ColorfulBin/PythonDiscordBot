import discord
from discord.ext import commands
import random


class games_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.play = ["None", "None"]
        self.r_number = ["None"]
        pass

    @commands.Cog.listener()
    async def on_message(self, ctx):
        if self.play[0] == "None":
            pass
        elif self.play[0] == "r_number":
            if self.r_number[0] == ctx.content and self.play[1] == ctx.channel.id:
                embed = discord.Embed(title="Number Guessed!",
                                      description=f"Hooray! {ctx.author.mention} first wrote guessed number - {self.r_number[0]}! :partying_face:",
                                      color=discord.Color.green())
                await ctx.add_reaction("🎉")
                await ctx.channel.send(embed=embed)
                self.play[0] = "None"
                self.r_number[0] = "None"

    @commands.command(
        name="numbers",
        aliases=["nums"],
        help="Starts new game: numbers"
    )
    async def numbers(self, ctx, *lim: str):
        try:
            low, high = int(lim[0]), int(lim[1])
            self.play[0] = "r_number"
            self.play[1] = ctx.channel.id
            self.r_number[0] = str(random.randint(low, high))
            embed = discord.Embed(title="Game Started!",
                                  description=f"Send your guesses in the chat! :smile:",
                                  color=discord.Color.green())
            await ctx.send(embed=embed)
        except ValueError:
            embed = discord.Embed(title="Request Handle Error",
                                  description="It does-sn't look like a number! :worried:",
                                  color=discord.Color.red())
            await ctx.send(embed=embed, delete_after=5.0)
            await ctx.message.add_reaction("❌")
        except IndexError:
            try:
                high = int(lim[0])
                self.play[0] = "r_number"
                self.play[1] = ctx.channel.id
                self.r_number[0] = str(random.randint(1, high))
                embed = discord.Embed(title="Game Started!",
                                      description=f"Send your guesses in the chat! :smile:",
                                      color=discord.Color.green())
                await ctx.send(embed=embed)
            except ValueError:
                embed = discord.Embed(title="Request Handle Error",
                                      description="It does-sn't look like a number! :worried:",
                                      color=discord.Color.red())
                await ctx.send(embed=embed, delete_after=5.0)
                await ctx.message.add_reaction("❌")


async def setup(bot):
    await bot.add_cog(games_cog(bot))
