import discord
from discord.ext import commands

client = commands.Bot(command_prefix='.')
# holds instance of my bot


@client.event
async def on_ready():
    print('Bot logged in as {0.user}'.format(client))


@client.command()
async def help_me(ctx):
    await ctx.send("Hello I'm  and here are some commands you may have want to use:")


@client.command()
async def bot_latency(ctx):
    await ctx.send(f'Hey, my ping is {round(client.latency * 1000)}ms.')


@client.command()
async def hey(ctx):
    author = ctx.message.author.name
    await ctx.send(f'Hello {author} jesteś koks')


@client.command()
async def clear_msg(ctx, amount=2, onlybot='no'):
    def is_me(m):
        return m.author == client.user
    if onlybot == 'only_bot':
        await ctx.channel.purge(limit=amount, check=is_me)
    else:
        await ctx.channel.purge(limit=amount)


@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member):
    await ctx.send(f'{member} was kicked')
    await member.kick(reason="")


@kick.error
async def kick_error(ctx, error):
    await ctx.send(f"You can't kick that member \n error is {error}")


token_file = open("token.txt", "r")
token = token_file.readline()
client.run(token)
