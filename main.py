if __name__ == "__main__":
    try:
        import discord
        from discord.ext import commands
        import os
        import ctypes
        from jokeapi import Jokes
        import random
        import string
        import yt_dlp
        import asyncio
        import json
        import aiohttp
        from rgbprint import rgbprint
        from general.printer import terminal_starter
    except ModuleNotFoundError:
        import os
        os.system(" ")
        print("\033[91mDidn't install needed modules. Installing them now\033[0m")
        os.system("pip install discord")
        os.system("pip install jokeapi")
        os.system("pip install yt_dlp")
        os.system("pip install asyncio")
        os.system("pip install rgbprint")
        os.system("pip install aiohttp")
        print("\033[91mSuccessfully installed required modules\033[0m")
        os.system("pause")
        exit(1)
    except FileNotFoundError:
        rgbprint("File 'printer.py' is not found! Reinstall files", color=(255, 0, 0))
        os.system("pause")
        exit(1)

    os.system(" ")
    directory = os.getcwd()
    with open(fr"{directory}\general\token.txt", "r") as i:
        token = i.readlines()[0]
    if token == "token":
        rgbprint("Start Error\n-----------\nToken not found. Seems you haven't changed it!", color=(255, 0, 0))
        os.system("pause")
        exit(1)

    terminal_starter()
    intents = discord.Intents.default()
    intents.members = True
    intents.message_content = True
    bot = commands.Bot(command_prefix=">", description="Help function is not finished yet (since 20.04)", intents=intents)

    @bot.event
    async def on_ready():
        try:
            await bot.load_extension("cogs.general_cog")
            await bot.load_extension("cogs.music_cog")
            await bot.load_extension("cogs.games_cog")
            await bot.load_extension("cogs.horny_cog")
        except discord.ext.commands.errors.ExtensionNotFound:
            rgbprint("Cogs run error! Reinstall files", color=(255, 0, 0))
            os.system("pause")
            exit(1)

    bot.run(token)
