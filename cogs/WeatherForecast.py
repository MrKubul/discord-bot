import asyncio
import requests
import datetime
from bs4 import BeautifulSoup
from discord.ext import commands

time_now = datetime.datetime.now()


class WeatherForecast(commands.Cog):
    def __init__(self, client):
        self.client = client

    def weather_scrapper(self, city):
        url = 'https://meteobox.pl/' + city + '/'
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36"}
        page = requests.get(url, headers=headers)
        parsed_page = BeautifulSoup(page.content, 'html.parser')
        temperatures = parsed_page.findAll(class_='potemp')
        current_id = 'tp' + str(time_now.year).zfill(4) + str(time_now.month).zfill(2) + str(time_now.day).zfill(2)
        description_today = parsed_page.find(id=current_id)
        weather_data = [temperatures, description_today]
        return weather_data

    @commands.command()
    async def weather_today(self, ctx, *, city):
        await ctx.send(f'Searching for weather in {city.capitalize()}...')
        await asyncio.sleep(2)
        city = city.replace(' ', '-')
        data = self.weather_scrapper(city)
        data = data[1].text.replace('2020', '2020.\n\n')
        try:
            await ctx.send(f'{data}')
        except Exception as e:
            await ctx.send("You probably spelled that wrong")
            print(e)

    @commands.command()
    async def temperature_in(self, ctx, days: int, *, city):
        if 0 > days or days > 4:
            await ctx.send(f'Wrong number of days, need to be between 0 and 4')
            return
        await ctx.send(f'Searching for temperature in {city.capitalize()}...')
        await asyncio.sleep(2)
        city = city.replace(' ', '-')
        weather_data = self.weather_scrapper(city)
        try:
            temp = weather_data[0][days].text
            new_time = time_now + datetime.timedelta(days=days)
            await ctx.send(f'On day {new_time.day} of {new_time.strftime("%B")} {new_time.year} will be equal to {temp}')
        except Exception as e:
            await ctx.send(
                "You probably spelled that wrong! Remember to write it in lower case and without polish signs!")
            print(e)


def setup(client):
    client.add_cog(WeatherForecast(client))
