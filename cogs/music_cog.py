import discord
from discord.ext import commands
import os
import yt_dlp
import asyncio


class music_cog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.is_playing = None
        self.is_paused = None
        self.current_song = None
        self.queue = []
        self.current_volume = 1
        self.directory = os.getcwd()
        self.ytdl_format_options = dict(format="worstaudio/best", restrictfilenames=True, noplaylist=True,
                                        nocheckcertificate=True,
                                        ignoreerrors=False, logtostderr=False, quiet=True, no_warnings=True,
                                        default_search="auto",
                                        source_address="0.0.0.0")
        self.ffmpeg_options = {"options": "-vn"}
        self.ytdl = yt_dlp.YoutubeDL(self.ytdl_format_options)

    async def playing(self, ctx):

        def after_played():
            self.is_playing = False
            self.queue.pop(0)

        while True:
            await asyncio.sleep(1)
            if not self.is_playing and not self.is_paused and self.queue:
                self.current_song = self.queue[0]
                self.is_playing = True
                ctx.guild.voice_client.play(discord.FFmpegPCMAudio(executable=fr"{self.directory}\cogs\ffmpeg\ffmpeg.exe", source=fr"{self.directory}\cogs\songs\{self.current_song}"), after=lambda e: after_played())

    async def change_is_playing(self):
        self.is_playing = not self.is_playing
        self.queue.pop(0)

    @commands.command(
        name="play",
        aliases=["pl", "add", "dd"],
        help="Plays the added song or adds it to queue")
    async def play(self, ctx, search: str):
        if not search:
            embed = discord.Embed(title="URL Error",
                                  description="Wh-here is the song URL? :worried:",
                                  color=discord.Color.red())
            await ctx.channel.send(embed=embed, delete_after=5.0)
            await ctx.message.add_reaction("❌")
        elif ctx.author.voice:
            try:
                await ctx.author.voice.channel.connect()
            except:
                await ctx.guild.voice_client.move_to(ctx.author.voice.channel)
            os.chdir(fr"{self.directory}\cogs\songs")
            data = self.ytdl.extract_info(search, download=True)
            os.chdir(self.directory)
            if "entries" in data:
                data = data["entries"][0]
            self.queue.append(self.ytdl.prepare_filename(data))
            await self.bot.loop.create_task(await self.playing(ctx))
        else:
            embed = discord.Embed(title="User Error",
                                  description="B-but you are not in-n voice channel! :worried:",
                                  color=discord.Color.red())
            await ctx.channel.send(embed=embed, delete_after=5.0)
            await ctx.message.add_reaction("❌")

    @commands.command(
        name="stop",
        aliases=["st"],
        help="Stops the current song")
    async def pause(self, ctx):
        if self.is_playing:
            self.is_playing = False
            self.is_paused = True
            vc = ctx.guild.voice_client
            vc.pause()
            await ctx.channel.send(f"{ctx.author.mention}, I stopped the song in your voice channel :smile:")
        else:
            embed = discord.Embed(title="Stop Error",
                                  description="I don't pl-lay anything already! :worried:",
                                  color=discord.Color.red())
            await ctx.channel.send(embed=embed, delete_after=5.0)
            await ctx.message.add_reaction("❌")

    @commands.command(
        name="resume",
        aliases=["rs"],
        help="Resumes the last song added")
    async def resume(self, ctx):
        if not self.is_playing:
            self.is_playing = None
            self.is_paused = False
            await ctx.channel.send(f"{ctx.author.mention}, I resumed the songs in your voice channel :smile:")
            await self.playing(ctx)
        else:
            embed = discord.Embed(title="Resume Error",
                                  description="I pl-lay something already! :worried:",
                                  color=discord.Color.red())
            await ctx.channel.send(embed=embed, delete_after=5.0)
            await ctx.message.add_reaction("❌")

    @commands.command(
        name="volume",
        aliases=["vl"],
        help="Sets up new volume of bot"
    )
    async def volume(self, ctx, volume: str):
        vc = ctx.message.guild.voice_client
        if volume.endswith("%"):
            volume = volume.split("%")[0]
        try:
            volume = int(volume)
        except:
            embed = discord.Embed(title="Volume Error",
                                  description="I d-don't undertand this number! :worried:",
                                  color=discord.Color.red())
            await ctx.channel.send(embed=embed, delete_after=5.0)
            await ctx.message.add_reaction("❌")
            return
        if 0 <= volume <= 100:
            volume = volume / 100
            vc.source = discord.PCMVolumeTransformer(vc.source, volume=volume/self.current_volume)
            self.current_volume = volume
        else:
            embed = discord.Embed(title="Volume Error",
                                  description="Your volume loo-oks strange! :worried:",
                                  color=discord.Color.red())
            await ctx.channel.send(embed=embed, delete_after=5.0)
            await ctx.message.add_reaction("❌")

    @commands.command(
        name="skip",
        aliases=["sk"],
        help="Skips current song"
    )
    async def skip(self, ctx):
        vc = ctx.guild.voice_client
        await vc.stop()
        if self.queue and self.is_playing and not self.is_paused:
            await self.pause(self, ctx)
            self.queue.pop(0)
            await self.resume(self, ctx)
            await ctx.channel.send("I skipped this song! :smile:")
        else:
            embed = discord.Embed(title="Skip Error",
                                  description="I have nothi-ing to play already! :worried:",
                                  color=discord.Color.red())
            await ctx.channel.send(embed=embed, delete_after=5.0)
            await ctx.message.add_reaction("❌")

    @commands.command(
        name="disconnect",
        aliases=["dsc", "kys"],
        help="Disconnects from users voice channel"
    )
    async def disconnect(self, ctx):
        if ctx.guild.voice_client:
            vc = ctx.guild.voice_client
            await vc.disconnect()
            embed = discord.Embed(title="Disconnected",
                                  description=f"I'm out! Wish I could help you, {ctx.author.name} :smile:",
                                  color=discord.Color.green())
            await ctx.channel.send(embed=embed, delete_after=5.0)
        else:
            embed = discord.Embed(title="Disconnect Error",
                                  description="I'm not in voice channel already! :worried:",
                                  color=discord.Color.red())
            await ctx.channel.send(embed=embed, delete_after=5.0)
            await ctx.message.add_reaction("❌")


async def setup(bot):
    await bot.add_cog(music_cog(bot))
