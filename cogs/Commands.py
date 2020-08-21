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

    @commands.command()
    async def logout(self, ctx):
        await ctx.message.add_reaction('✅')
        print("Bot logged out successfully!")
        await self.client.logout()

    @commands.command()
    async def help_me(self, ctx):
        embed = discord.Embed(description="Hello I'm KuBot and here is list of  useful commands you may have want to use. If some commands or features don't work contact the creator.")
        embed.set_author(name='KuBot', icon_url=self.client.user.avatar_url)
        embed.add_field(name="CREATOR COMMANDS",value="_", inline=False)
        embed.add_field(name="1. $load <name_of_extension>", value="loads extension to bot", inline=False)
        embed.add_field(name="2. $unload <name_of_extension>", value="unloads extension to bot", inline=False)
        embed.add_field(name="3. $reload <name_of_extension>", value="reloads extension to bot", inline=False)
        embed.add_field(name="WEATHER FORECAST COMMANDS", value="_", inline=False)
        embed.add_field(name="1. $weather_today <name of city>", value="prints full weather description ,today in that city", inline=False)
        embed.add_field(name="$temperature_in <days> <name of city>", value="prints temperature in that city in X days from today", inline=False)
        embed.add_field(name="GENERAL COMMANDS", value="_", inline=False)
        embed.add_field(name="1. $bots_latency", value="prints actual bot latency.", inline=False)
        embed.add_field(name="2. $hey", value="say hi to bot.", inline=False)
        embed.add_field(name="3. $logout", value="bot turns off.", inline=False)
        embed.add_field(name="3. $logout", value="bot turns off.", inline=False)
        embed.add_field(name="4. $clear_msg <amount> <onlybot>", value="deletes last X messages, add only_bot if you want to delete bots messages only.", inline=False)
        embed.add_field(name="MODERATION COMMANDS", value="_", inline=False)
        embed.add_field(name="1. $kick <member> <reason>", value="kicks that member, mind you need to tag them with '@'.", inline=False)
        await ctx.send(embed=embed)


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
