import discord
from discord.ext import commands


class Cmds(commands.Cog):
    def __init__(self, client):
        self.client = client

    ### basic commands

    @commands.command()
    async def hey(self, ctx):
        author = ctx.message.author.name
        await ctx.send(f'Hello {author} jesteś koks')

    @commands.command()
    async def help_me(self, ctx):
        await ctx.send("Hello I'm  and here are some commands you may have want to use:")

    @commands.command()
    async def bots_latency(self, ctx):
        await ctx.send(f'Hey, my ping is {round(self.client.latency * 1000)}ms.')

    @commands.command()
    async def clear_msg(self, ctx, amount=2, onlybot='no'):
        def is_me(m):
            return m.author == self.client.user

        if onlybot == 'only_bot':
            await ctx.channel.purge(limit=amount, check=is_me)
        else:
            await ctx.channel.purge(limit=amount)

    ###moderation commands

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member):
        await ctx.send(f'{member} was kicked')
        await member.kick(reason="")

    @kick.error
    async def kick_error(self, ctx, error):
        await ctx.send(f"You can't kick that member. \n Because {error}")


def setup(client):
    client.add_cog(Cmds(client))
