import discord
from discord.ext import commands
from discord.utils import get


class MusicBot(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def join(self, ctx):
        if ctx.message.author.voice:
            channel = ctx.message.author.voice.channel
            await channel.connect()

    @commands.command()
    async def leave(self, ctx):
        if ctx.message.author.voice:
            channel = ctx.message.author.voice.channel
            voice_client = get(self.client.voice_clients, guild=ctx.guild)
            await voice_client.disconnect()

def setup(client):
    client.add_cog(MusicBot(client))
