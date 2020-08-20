import asyncio
import discord
from discord.ext import commands


class Commmands(commands.Cog):
    def __init__(self, client):
        self.client = client

# Basic commands:

    @commands.command()
    async def hey(self, ctx):
        author = ctx.message.author.name
        await ctx.send(f'Hello {author}, you are koks')


    @commands.command() # TODO segregate commands into categories in command help_me#
    async def help_me(self, ctx):
        await ctx.send("Hello I'm KuBot and here is list of  useful commands you may have want to use:")
        await ctx.send("If some commands or features don't work contact the creator.")
        await asyncio.sleep(4)
        await ctx.send("1. $load <name_of_extension> - loads extension to bot")
        await ctx.send("2. $unload <name_of_extension> - unloads extension to bot")
        await ctx.send("3. $reload <name_of_extension> - reloads extension to bot")
        await ctx.send("4. $bots_latency - prints actual bot latency.")
        await ctx.send("5. $clear_msg <amount> <onlybot> - deletes last X messages, add only_bot if you want to delete bots messages only.")
        await ctx.send("6. $kick <member> <reason> - kicks that member, mind you need to tag them with '@'.")



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

# Moderation commands:

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member):
        await ctx.send(f'{member} was kicked')
        await member.kick(reason="")

    @kick.error
    async def kick_error(self, ctx, error):
        await ctx.send(f"You can't kick that member. \n {error}")


def setup(client):
    client.add_cog(Commmands(client))
