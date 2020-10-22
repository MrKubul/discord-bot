import shutil
import urllib.request
import re
import discord
import os
import youtube_dl
from discord.ext import commands
from discord.utils import get


class MusicBot(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True, aliases=['j'])
    async def join(self, ctx):
        if ctx.message.author.voice is None:
            await ctx.send(f'Join voice channel first')
            return

        channel = ctx.message.author.voice.channel
        voice_client = get(self.client.voice_clients, guild=ctx.guild)

        if voice_client and voice_client.is_connected():
            await voice_client.move_to(channel)
            await self.client.change_presence(activity=discord.Game(f'connected to {channel}'))
        else:
            await channel.connect()
            await ctx.send(f'Bot connected to {channel}')
            await self.client.change_presence(activity=discord.Game(f'connected to {channel}'))

    @commands.command(pass_context=True, aliases=['l'])
    async def leave(self, ctx):
        voice_client = get(self.client.voice_clients, guild=ctx.guild)
        if voice_client is None:
            await ctx.send(f'no bot in any voice channel')
            return

        channel = ctx.message.author.voice.channel

        if voice_client and voice_client.is_connected():
            await voice_client.disconnect()
            await ctx.send(f'Bot disconnected from {channel}')
            await self.client.change_presence(activity=discord.Game('https://github.com/MrKubul/discord-bot'))
        else:
            await ctx.send(f"Bot isn't connected to any voice channel")

    def retrieve_yt_url(self, name):
        name = name.replace(' ', '+')
        html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + name)
        video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
        try:
            url = "https://www.youtube.com/watch?v=" + str(video_ids[0])
        except:
            print("song not found on yt")
        return url

    @commands.command(pass_context=True, aliases=['p'])
    async def play(self, ctx, *, song_name: str):

        def check_queue():
            queue_in_file = os.path.isdir("./Queue")
            if queue_in_file is True:
                DIR = os.path.abspath(os.path.realpath("Queue"))
                length = len(os.listdir(DIR))
                try:
                    first_file = os.listdir(DIR)[0]
                except:
                    print("No more queued song(s)\n")
                    self.queues.clear()
                    self.queue_names.clear()
                    return
                holder = os.path.dirname(os.path.realpath(__file__))
                main_location = os.path.dirname(holder)
                song_path = os.path.abspath(os.path.realpath("Queue") + "\\" + first_file)
                if length != 0:
                    self.queue_names.pop()
                    print("Song done, playing next queued\n")
                    song_there = os.path.isfile("song.mp3")
                    if song_there:
                        os.remove("song.mp3")
                    shutil.move(song_path, main_location)
                    for file in os.listdir("./"):
                        if file.endswith(".mp3"):
                            os.rename(file, 'song.mp3')

                    voice_client.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: check_queue())
                    voice_client.source = discord.PCMVolumeTransformer(voice_client.source)
                    voice_client.source.volume = 0.07

                else:
                    self.queues.clear()
                    self.queue_names.clear()
                    return

            else:
                self.queues.clear()
                self.queue_names.clear()
                print("No songs were queued before the ending of the last song\n")

        url = self.retrieve_yt_url(song_name)
        is_song_downloaded = os.path.isfile('song.mp3')
        try:
            if is_song_downloaded:
                os.remove('song.mp3')
                self.queues.clear()
                self.queue_names.clear()
                print("previous song was removed")
        except PermissionError:
            ctx.send('music is currently playing')

        Queue_infile = os.path.isdir("./Queue")
        try:
            Queue_folder = "./Queue"
            if Queue_infile is True:
                print("Removed old Queue Folder")
                shutil.rmtree(Queue_folder)
        except:
            print("No old Queue folder")

        voice_client = get(self.client.voice_clients, guild=ctx.guild)
        if voice_client is None:
            await ctx.send('connect bot to audio channel to play music')
            return
        if voice_client.is_playing():
            await ctx.send("Bot currently playing wait till end")
            return

        ydl_options = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        with youtube_dl.YoutubeDL(ydl_options) as ydl:
            print("Downloading audio now...\n")
            ydl.download([url])

        for file in os.listdir("./"):
            if file.endswith(".mp3"):
                global name
                name = file
                print(f"Renamed File: {file}\n")
                os.rename(file, "song.mp3")

        voice_client.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: check_queue())
        voice_client.source = discord.PCMVolumeTransformer(voice_client.source)
        voice_client.source.volume = 0.07

        newname = name.rsplit("-", 2)
        await ctx.send(f"Playing: {newname[0]}")
        await self.client.change_presence(activity=discord.Game(f'playing music'))

    queues = {}
    queue_names = []

    @commands.command(pass_context=True, aliases=['q'])
    async def queue(self, ctx, *, song_name: str):
        url = self.retrieve_yt_url(song_name)
        is_queue_fle = os.path.isdir("./Queue")
        if is_queue_fle is False:
            os.mkdir("Queue")
        DIR = os.path.abspath(os.path.realpath("Queue"))
        q_num = len(os.listdir(DIR))
        q_num += 1  # adding new song to number of song queued
        while q_num in self.queues:
            q_num += 1
        self.queues[q_num] = q_num

        queue_path = os.path.abspath(os.path.realpath("Queue") + f"\song{q_num}.%(ext)s")

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': queue_path,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        await ctx.send("Adding " + song_name + " at " + str(q_num) + ' in queue')
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            print("Downloading audio now\n")
        self.queue_names.append(song_name)
        print("Song added to queue\n")

    @commands.command(pass_context=True)
    async def print_queue(self, ctx):
        it = 1
        for song in self.queue_names:
            await ctx.send(str(it) + '. ' + song)
            it += 1

    @commands.command(pass_context=True)
    async def pause(self, ctx):
        voice_client = get(self.client.voice_clients, guild=ctx.guild)

        if voice_client and voice_client.is_playing():
            voice_client.pause()
            await ctx.send("Music paused")
        else:
            await ctx.send("Music not playing failed pause")

    @commands.command(pass_context=True, aliases=['r'])
    async def resume(self, ctx):
        voice_client = get(self.client.voice_clients, guild=ctx.guild)

        if voice_client and voice_client.is_paused():
            voice_client.resume()
            await ctx.send("Resumed music")
        else:
            await ctx.send("Music is not paused")

    @commands.command(pass_context=True, aliases=['s'])
    async def skip(self, ctx):
        voice_client = get(self.client.voice_clients, guild=ctx.guild)

        if voice_client and voice_client.is_playing():
            voice_client.stop()
            await ctx.send("Music skipped")
        else:
            await ctx.send("No music playing failed to stop")


def setup(client):
    client.add_cog(MusicBot(client))
