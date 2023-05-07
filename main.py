if __name__ == "__main__":
    class bcolors:
        HEADER = "\033[95m"
        OKBLUE = "\033[94m"
        OKCYAN = "\033[96m"
        OKGREEN = "\033[92m"
        WARNING = "\033[93m"
        FAIL = "\033[91m"
        ENDC = "\033[0m"
        BOLD = "\033[1m"
        UNDERLINE = "\033[4m"
    try:
        import discord
        from discord.ext import commands
        import os
        from jokeapi import Jokes
        import random
        import string
        import yt_dlp
        import asyncio
        from general.terminal_starter import terminal_starter
    except ModuleNotFoundError:
        import os
        os.system(" ")
        print(f"{bcolors.HEADER}Didn't install needed modules. Installing them now{bcolors.ENDC}")
        os.system("pip install discord")
        os.system("pip install jokeapi")
        os.system("pip install yt_dlp")
        os.system("pip install asyncio")
        os.system("python -m pip install discord")
        os.system("python -m pip install jokeapi")
        os.system("python -m pip install yt_dlp")
        os.system("python -m pip install asyncio")
        print(f"{bcolors.HEADER}Successfully installed required modules{bcolors.ENDC}")
        os.system("pause")
        exit(1)

    os.system(" ")
    directory = os.getcwd()
    with open(fr"{directory}\general\token.txt", "r") as i:
        token = i.readlines()[0]
    if token == "token":
        print(f"{bcolors.FAIL}Start Error{bcolors.ENDC}")
        print(f"-----------")
        print(f"{bcolors.OKGREEN}Token not found. Seems you haven't changed it!{bcolors.ENDC}")
        os.system("pause")
        exit(1)

    terminal_starter()
    intents = discord.Intents.default()
    intents.members = True
    intents.message_content = True
    bot = commands.Bot(command_prefix=">",
                       description="Help function is not finished yet (since 20.04)",
                       intents=intents)

    @bot.event
    async def on_ready():
        try:
            await bot.load_extension("cogs.general_cog")
            await bot.load_extension("cogs.music_cog")
            await bot.load_extension("cogs.games_cog")
        except discord.ext.commands.errors.ExtensionNotFound:
            print(f"{bcolors.FAIL}Cogs run error! Reinstall files{bcolors.ENDC}")
            os.system("pause")
            exit(1)

    bot.run(token)
