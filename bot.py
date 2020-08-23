import sqlite3
import discord
import os
from discord.ext import commands

client = commands.Bot(command_prefix='$')

connection = sqlite3.connect('member_base.s3db')
cursor = connection.cursor()


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game("https://github.com/MrKubul/discord-bot"))
    print('Bot logged in as {0.user}'.format(client))
    with connection:
        cursor.execute(
            'CREATE TABLE IF NOT EXISTS member_base ( user_id TEXT, level INTEGER, experience INTEGER, balance INTEGER)')
    for guild in client.guilds:
        if guild.id == 707341420926730334:  # here paste your server id !!
            for member in guild.members:
                if not member.bot:
                    with connection:
                        cursor.execute('SELECT * from member_base WHERE (user_id=?)', (str(member.id),))
                        if cursor.fetchone() is None:
                            params = (str(member.id), 1, 0, 0)
                            with connection:
                                cursor.execute('INSERT INTO member_base VALUES (?, ?, ?, ?)', params)
                                print(f'{member} was inserted to database')
    with connection:
        cursor.execute('SELECT * FROM member_base')
    data = cursor.fetchall()
    print(data)
    print("Database update ended")


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
