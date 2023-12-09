import discord
from discord.ext import commands, tasks
import random
import asyncio
import config
import openai
import interactions



intents = discord.Intents().all()
client = commands.Bot(command_prefix='!', intents=intents)
client.remove_command("help")
openai.api_key = config.token_openai


@client.event
async def on_ready():
    print(f'Logged in as {client.user.name}')

@client.slash_command(name='ping', description="Показывает пинг")
             
async def ping(ctx):
    await ctx.delete()
    await ctx.send(f'Скорость бота - {round(client.latency * 1000)}мс')

@client.slash_command(name='8ball')
async def eightball(ctx, *, question):
    responses = ["Бесспорно.",
                 "Предрешено.",
                 "Никаких сомнений.",
                 "Определённо да.",
                 "Можешь быть уверен в этом.",
                 "Мне кажется да.",
                 "Вероятнее всего.",
                 "Хорошие перспективы.",
                 "Знаки говорят да.",
                 "Да.",
                 "Пока не ясно, попробуй снова.",
                 "Спроси позже.",
                 "Лучше не рассказывать.",
                 "Сейчас нельзя предсказать.",
                 "Сконцентрируйся и спроси опять.",
                 "Даже не думай.",
                 "Мой ответ нет.",
                 "По моим данным нет.",
                 "Перспективы не очень хорошие.",
                 "Весьма сомнительно.",
                 "Нет."
                 ]
    await ctx.delete()
    await ctx.send(f':8ball: Вопрос: {question}\n:8ball: Ответ: {random.choice(responses)}')


@client.slash_command(name='remind', description='Time - Время: Секунды = s, Минуты = m, Часы = h, Дни = d; Task - Напоминание.')
async def remind(ctx, time, * ,task):
    def convert(time):
        pos = ['s', 'm', 'h', 'd']

        time_dict = {"s": 1, "m": 60, "h": 3600, "d": 3600*24}

        unit = time[-1]

        if unit not in pos:
            return -1
        try:
            val = int(time[:-1])
        except:
            return -2
 
        return val * time_dict[unit]
    
    converted_time = convert(time)

    if converted_time == -1:
        await ctx.send("Ты написал(а) время неправильно.")
        return
    
    if converted_time == -2:
        await ctx.send("Время должно быть целым числом.")
        return
    
    await ctx.send(f'Напоминание запущено ***{task}*** и продлится ***{time}***.')
    await ctx.delete()
    await asyncio.sleep(converted_time)
    await ctx.send(f"{ctx.author.mention} твое напоминание ***{task}*** завершилось.")

@client.slash_command(name='gpt')
async def cont(ctx: commands.context, * , args):
  result = str(args)
  response = openai.Completion.create(
  model="text-davinci-003",
  prompt=result,
  temperature=0.5,
  max_tokens=60,
  top_p=1.0,
  frequency_penalty=0.5,
  presence_penalty=0.0,
  stop=["You:"]
)
  await ctx.delete()
  await ctx.send(embed=discord.Embed(title=f'{result}', description=response['choices'][0]['text']))
'''
@client.slash_command(name='clear', description='Очищает сообщаения')
async def clear(ctx, amount:int):
    interactionResponse = ctx.response
    await ctx.channel.purge(limit=amount)
    await ctx.send(f"Я очистила {amount} сообщений!")
    await interactionResponse.defer()
    await asyncio.sleep(1)
    await ctx.channel.purge(limit=amount)
    await ctx.delete()
'''

@client.slash_command(name='clear', description='Очищает сообщаения')
async def clear(ctx, amount:int):
    await ctx.channel.purge(limit=amount)
    await ctx.delete()

client.run(config.token)