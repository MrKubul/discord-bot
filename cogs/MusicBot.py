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
        elif channel:
            await channel.connect()
            await ctx.send(f'Bot connected to {channel}')
            await self.client.change_presence(activity=discord.Game(f'connected to {channel}'))

    @commands.command(pass_context=True, aliases=['l'])
    async def leave(self, ctx):
        if ctx.message.author.voice is None:
            await ctx.send(f'no bot in any voice channel')
            return

        channel = ctx.message.author.voice.channel
        voice_client = get(self.client.voice_clients, guild=ctx.guild)

        if voice_client and voice_client.is_connected():
            await voice_client.disconnect()
            await ctx.send(f'Bot disconnected from {channel}')
            await self.client.change_presence(activity=discord.Game('https://github.com/MrKubul/discord-bot'))
        else:
            ctx.send(f"Bot isn't connected to any voice channel")

    @commands.command(pass_context=True, aliases=['p'])
    async def play(self, ctx, url: str):
        is_song_downloaded = os.path.isfile('song.mp3')
        try:
            if is_song_downloaded:
                os.remove('song.mp3')
                print("previous song was removed")
        except PermissionError:
            ctx.send('music is currently playing')

        voice_client = get(self.client.voice_clients, guild=ctx.guild)

        ydl_options = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        with youtube_dl.YoutubeDL(ydl_options) as ydl:
            print("Downloading audio now\n")
            ydl.download([url])

        for file in os.listdir("./"):
            if file.endswith(".mp3"):
                name = file
                print(f"Renamed File: {file}\n")
                os.rename(file, "song.mp3")

        voice_client.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: self.client.change_presence(activity=discord.Game(f'connected to {ctx.message.channel}')))
        await self.client.change_presence(activity=discord.Game(f'playing music'))
        voice_client.source = discord.PCMVolumeTransformer(voice_client.source)
        voice_client.source.volume = 0.07

        await ctx.send(f'Playing: {name}')


def setup(client):
    client.add_cog(MusicBot(client))
