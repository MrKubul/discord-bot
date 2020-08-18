# import discord
from discord.ext import commands

client = commands.Bot(command_prefix='.')


@client.event
async def on_ready():
    print('Bot logged in as {0.user}'.format(client))


@client.command()
async def help_me(ctx):
    await ctx.send("Hello I'm KuBot and here are some commands you may have want to use:")


token_file = open("token.txt", "r")
token = token_file.readline()
client.run(token)
