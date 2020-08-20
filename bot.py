import discord
import os
import asyncio
from discord.ext import commands

client = commands.Bot(command_prefix='$')


@client.event
async def on_ready():
    print('Bot logged in as {0.user}'.format(client))


@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')
    await ctx.send(f'{extension} has been loaded successfully.')


@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    await ctx.send(f'{extension} has been unloaded successfully.')


@client.command()
async def reload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')
    await ctx.send(f'{extension} has been reloaded successfully.')


for file in os.listdir('./cogs'):
    if file.endswith('.py'):
        client.load_extension(f'cogs.{file[:-3]}')

token_file = open("token.txt", "r")
token = token_file.readline()
client.run(token)
