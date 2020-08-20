import discord
import requests
from bs4 import BeautifulSoup
from discord.ext import commands


class WeatherForecast(commands.Cog):
    def __init__(self, client):
        self.client = client

    def weather_scrapper(self, city):
        url = 'https://meteobox.pl/' + city + '/'
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36"}
        page = requests.get(url, headers=headers)
        parsed_page = BeautifulSoup(page.content, 'html.parser')
        temperature = parsed_page.findAll(class_='potemp')
        return temperature

    @commands.command()
    async def weather_today(self, ctx, *, city):
        city = city.replace(' ', '-')
        temp = self.weather_scrapper(city)
        city = city.replace('-', ' ')
        await ctx.send(f'Searching for weather in {city.capitalize()}...')
        try:
            await ctx.send(f'Temperature is equal to {temp[0].text}')
        except Exception:
            await ctx.send("You probably spelled that wrong")

    @commands.command()
    async def weather_tommorow(self, ctx, *, city):
        city = city.replace(' ', '-')
        temp = self.weather_scrapper(city)
        city = city.replace('-', ' ')
        await ctx.send(f'Searching for weather in {city.capitalize()}...')
        try:
            await ctx.send(f'Tommorow temperature will be equal to {temp[1].text}')
        except Exception:
            await ctx.send("You probably spelled that wrong!")


def setup(client):
    client.add_cog(WeatherForecast(client))
