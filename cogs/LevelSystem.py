import sqlite3
import discord
import random
from discord.ext import commands


connection = sqlite3.connect('member_base.s3db')
cursor = connection.cursor()


class LevelSystem(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def check_for_promotion(self, user_id):
        with connection:
            cursor.execute('SELECT experience from member_base WHERE (user_id=?)', (str(user_id),))
            current_exp = cursor.fetchone()
            cursor.execute('SELECT level from member_base WHERE (user_id=?)', (str(user_id),))
            level_fetched = cursor.fetchone()
            level_to_process = int(level_fetched[0])
            current_exp_comparable = int(current_exp[0])
            if current_exp_comparable is not None and level_to_process is not None:
                if current_exp_comparable == level_to_process ** 2:
                    with connection:
                        cursor.execute('UPDATE member_base SET experience = 0')
                        cursor.execute('SELECT level from member_base WHERE (user_id=?)', (str(user_id),))
                        current_level = cursor.fetchone()
                        current_level_comparable = int(current_level[0])
                        if current_level_comparable is not None:
                            if current_level_comparable < 100:
                                with connection:
                                    cursor.execute('UPDATE member_base SET level = level+1 WHERE (user_id=?)', (str(user_id),))
                                    print(f'{self.client.get_user(user_id)} level up to {current_level_comparable + 1}')
                                    cursor.execute(f'UPDATE member_base SET balance = balance+{(current_level_comparable ** 2) // 2} WHERE (user_id=?)', (str(user_id),))
                            elif current_level_comparable == 100:
                                print(f'{user_id} has achieved 100 level')

    @commands.command()
    async def level(self, ctx, member_to_process: discord.Member = None):
        member_to_process = ctx.author if not member_to_process else member_to_process
        user_id = member_to_process.id
        print(member_to_process.id)
        with connection:
            cursor.execute('SELECT level from member_base WHERE (user_id=?)', (user_id,))
            current_level = cursor.fetchone()
            if current_level is not None:
                await ctx.send(f'{member_to_process.name}: {current_level[0]} level')

    @commands.command()
    async def balance(self, ctx, member: discord.Member = None):
        member = ctx.author if not member else member
        user_id = member.id
        with connection:
            cursor.execute('SELECT balance from member_base WHERE (user_id=?)', (user_id,))
            current_bal = cursor.fetchone()
            if current_bal is not None:
                await ctx.send(f'{member.name}: {current_bal[0]} balance')

    @commands.command()
    async def bet(self, ctx, amount: int):
        user_id = ctx.author.id
        with connection:
            cursor.execute('SELECT balance from member_base WHERE (user_id=?)', (user_id,))
            current_bal = cursor.fetchone()
            if current_bal is None:
                ctx.send('User not included in database yet')
            if current_bal[0] < amount:
                ctx.send('Not enough balance on account')
            else:
                res = random.choice("WL")
                if res == 'W':
                    await ctx.send(f'You won {amount * 2} coins')
                    with connection:
                        cursor.execute(f'UPDATE member_base SET balance = balance+{amount} WHERE (user_id=?)', (str(user_id),))
                else:
                    await ctx.send(f'You lost {amount} coins')
                    with connection:
                        cursor.execute(f'UPDATE member_base SET balance = balance-{amount} WHERE (user_id=?)', (str(user_id),))

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        user_id = message.author.id
        with connection:
            cursor.execute('SELECT * from member_base WHERE (user_id=?)', (user_id,))
            correct_user = cursor.fetchone()
            if correct_user is None:
                print('User not found')
            else:
                with connection:
                    cursor.execute('UPDATE member_base SET experience = experience+1 WHERE (user_id=?)', (str(user_id),))
                    await self.check_for_promotion(user_id)


def setup(client):
    client.add_cog(LevelSystem(client))
