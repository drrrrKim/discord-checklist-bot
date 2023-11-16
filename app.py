import os
import discord

from dotenv import load_dotenv
from discord.ext import commands, tasks
from service import choice_royal, choice_wonki_berry

load_dotenv()
path_dir = os.path.dirname(os.path.realpath(__file__))

# bot setting
token = os.environ.get("DISSCODE_TOKEN")
prefix = '/'

# discord intents setting
intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.message_content = True

# bot client 
bot = commands.Bot(command_prefix=prefix, intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.command()
async def hello(ctx):
    await ctx.send("bye")

@bot.command()
async def 원기베리(ctx, number: int):
    if number>25:
        await ctx.send('25개이하로 숫자를 다시 입력')
    else:
        t = await choice_wonki_berry.choice_wonki_berry(path_dir,number)
        embed = discord.Embed(
            title="원기베리",
        )
        cnt=0
        for idx in t:
            cnt+=1
            embed.add_field(name=f"{cnt}번째 결과", value=idx, inline=False)

        await ctx.send(embed=embed)

@bot.command()
async def 로얄(ctx, number: int):
    if number>25:
        await ctx.send('25개이하로 숫자를 다시 입력')
    else:
        t = await choice_royal.choice_royal(path_dir,number)
        embed = discord.Embed(
            title="로얄스타일",
        )
        cnt=0
        for idx in t:
            cnt+=1
            embed.add_field(name=f"{cnt}번째 결과", value=idx, inline=False)

        await ctx.send(embed=embed)

bot.run(token)

