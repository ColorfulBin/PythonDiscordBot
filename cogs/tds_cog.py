import discord
from discord.ext import commands
import os


class tds_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    class strat_buttons(discord.ui.View):

        author = None
        message = None

        async def on_timeout(self) -> None:
            for button in self.children:
                button.disabled = True
            await self.message.edit(view=self)

        @staticmethod
        async def strategies_print(mode, interaction):
            strategies = ""
            with open(fr"{os.getcwd()}\tds_files\{mode}.txt", "r") as file:
                lines = file.readlines()
                if lines[0] == "NO_EVENTS":
                    await interaction.response.send_message(f"Sadly, there's no events in TDS right now! :sob:", ephemeral=True)
                    return
                for line in lines:
                    if line.split(">")[0] == "NAME":
                        strategies += "**" + line.split('>')[1].replace('\n', '') + "**\n"
                    elif line.split(">")[0] == "INFO":
                        strategies += line.split('>')[1].replace('\n', '') + "\n"
                    elif line.split(">")[0] == "LINK":
                        strategies += "[Link](<" + line.split('>')[1].replace('\n', '') + ">)\n"
                    else:
                        strategies += "*Credits:" + line.split('>')[1].replace('\n', '') + "*\n\n\n"
            await interaction.response.send_message(f"Ok! Here are some {mode} mode strategies:\n\n{strategies}", ephemeral=True)

        @discord.ui.button(label="normal",
                           style=discord.ButtonStyle.primary)
        async def normal(self, interaction=discord.Interaction, button=discord.ui.Button):
            if self.author == interaction.user:
                await self.strategies_print("normal", interaction)
                await self.on_timeout()

        @discord.ui.button(label="molten",
                           style=discord.ButtonStyle.primary)
        async def molten(self, interaction=discord.Interaction, button=discord.ui.Button):
            if self.author == interaction.user:
                await self.strategies_print("molten", interaction)
                await self.on_timeout()

        @discord.ui.button(label="fallen",
                           style=discord.ButtonStyle.primary)
        async def fallen(self, interaction=discord.Interaction, button=discord.ui.Button):
            if self.author == interaction.user:
                await self.strategies_print("fallen", interaction)
                await self.on_timeout()

        @discord.ui.button(label="hardcore",
                           style=discord.ButtonStyle.primary)
        async def hardcore(self, interaction=discord.Interaction, button=discord.ui.Button):
            if self.author == interaction.user:
                await self.strategies_print("hardcore", interaction)
                await self.on_timeout()

        @discord.ui.button(label="event",
                           style=discord.ButtonStyle.primary)
        async def event(self, interaction=discord.Interaction, button=discord.ui.Button):
            if self.author == interaction.user:
                await self.strategies_print("event", interaction)
                await self.on_timeout()
    
    @commands.command(
        name="strategy",
        aliases=["strat"],
        help="Gives strats too certain mode!"
    )
    async def strategy(self, ctx):
        buttons = self.strat_buttons(timeout=30)
        buttons.author = ctx.author
        buttons.message = await ctx.channel.send(f"{ctx.author.mention}, what strat do you need? :smile: ", view=buttons)

    @commands.command(
        name="update",
        aliases=["upd", "log"],
        help="Gives short variant of TDS newest update log"
    )
    async def update_logs(self, ctx):
        with open(fr"{os.getcwd()}\tds_files\update_log.txt", "r") as file:
            log = file.readlines()
            title = log[0]
            description = "".join(log[1::])
            embed = discord.Embed(title=title, description=description, color=discord.Color.blue(), url="https://tds.fandom.com/wiki/V1.7.2")
            embed.set_image(url="https://static.wikia.nocookie.net/tower-defense-sim/images/a/a3/AcceleratorDemomanUpdate.jpg/revision/latest/scale-to-width-down/1000?cb=20230507132433")
            await ctx.channel.send(embed=embed)


async def setup(bot):
    await bot.add_cog(tds_cog(bot))
