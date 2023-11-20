import os
import discord 

from dotenv import load_dotenv
from typing import Optional
from discord.ext import commands
from discord import app_commands

from service import choice, maple_event, symbol_cost

load_dotenv()
path_dir = os.path.dirname(os.path.realpath(__file__))

# bot setting
# token = os.environ.get("DISSCODE_TOKEN")
token = os.environ.get("TEST_DISSCODE_TOKEN")

prefix = '/'

# discord custom emoji id
extreme_gold = os.environ.get("EXTREME_GOLD")
gc = os.environ.get("GC")
jh = os.environ.get("GH")
mvp = os.environ.get("MVP")
exp = os.environ.get("EXP")
vip_doping = os.environ.get("VIP_DOPING")
vip_exp = os.environ.get("VIP_EXP")

cernium = os.environ.get("CERNIUM")
hotel = os.environ.get("HOTEL")
odium = os.environ.get("ODIUM")
shangrila = os.environ.get("SHANGRILA")
arteria = os.environ.get("ARTERIA")
carcion = os.environ.get("CARCION")
urus = os.environ.get("URUS")

# discord intents setting
intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.message_content = True

# bot client 
bot = commands.Bot(command_prefix=prefix, intents=intents, help_command=commands.DefaultHelpCommand())

# choice_item
@bot.tree.command(name="원기베리",
                  description="숫자만입력해주세요")
async def 원기베리(interaction:discord.Interaction,
               갯수: app_commands.Range[int,1,25]):
    res_data = await choice.choice_wonki_berry(path_dir,갯수)
    embed = discord.Embed(
        title="원기베리",
    )
    for idx,val in enumerate(res_data, start=1):
        embed.add_field(name=f"{idx}번째 결과", value=val, inline=False)

    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="로얄",
                  description="숫자만입력해주세요")
async def 로얄(interaction:discord.Interaction,
             갯수: app_commands.Range[int,1,25]):
    res_data = await choice.choice_royal(path_dir, 갯수)
    embed = discord.Embed(
        title="로얄스타일",
    )
    for idx,val in enumerate(res_data, start=1):
        embed.add_field(name=f"{idx}번째 결과", value=val, inline=False)

    await interaction.response.send_message(embed=embed)

# symbol
@bot.tree.command(name="어센틱")
@app_commands.choices(
    그란디스=[
        app_commands.Choice(name='세르니움', value=2),
        app_commands.Choice(name='아르크스', value=3),
        app_commands.Choice(name='오디움', value=4),
        app_commands.Choice(name='도원경', value=5),
        app_commands.Choice(name='아르테리아', value=6),
        app_commands.Choice(name='카르시온', value=7),
    ]
)
async def symbol_calc(interaction:discord.Interaction,
                      그란디스: app_commands.Choice[int],
                      시작레벨: app_commands.Range[int,1,11],
                      목표레벨: app_commands.Range[int,1,11]):
    if 시작레벨>=목표레벨:
        await interaction.response.send_message("시작레벨은 목표레벨보다 낮아야합니다.")
    else:
        price, symbol  = await symbol_cost.symbol_cost(path_dir,그란디스.value,시작레벨,목표레벨)
        embed = discord.Embed(
            title=f"{그란디스.name} {시작레벨}레벨에서 {목표레벨}레벨까지 심볼비용은?",
        )
        price = f'{price:,.0f}'
        
        embed.add_field(name="심볼(개)", value=symbol, inline=False)
        embed.add_field(name="가격(메소)", value=price, inline=False)

        await interaction.response.send_message(embed=embed)

@bot.command()
async def 좩(ctx):
    checklist_message = await ctx.send(f"재획 List:\n\n{jh} 재획비\n{gc} 경축비\n{mvp} 경뿌 \n{exp} 2배 \n{extreme_gold} 익골\n{vip_exp} vip")
    for emoji in [extreme_gold,gc,jh,mvp,exp,vip_exp ]:
        await checklist_message.add_reaction(emoji)

@bot.command()
async def 보스(ctx):
    checklist_message = await ctx.send(f"{vip_doping} vip\n")
    for emoji in [vip_doping ]:
        await checklist_message.add_reaction(emoji)

@bot.command()
async def 데일리(ctx):
    embed = discord.Embed(
            title="데일리 숙제",
        )
    str_t =f"{cernium} 세르니움\n{hotel} 호텔\n{odium} 오디움\n{shangrila} 도원경 \n{arteria} 아르테리아\n{carcion} 카르시온\n{urus}우르스"
    embed.add_field(name="",value=str_t, inline=False)
    daily_message =await ctx.send(embed=embed)

    for emoji in [cernium,hotel,odium,shangrila,arteria,carcion,urus]:
        await daily_message.add_reaction(emoji)

@bot.command()
async def 이벤트(ctx):
    embed = discord.Embed(
            title="진행중인이벤트",
        )
    str_t = await maple_event.maple_event()
    embed.add_field(name="",value=str_t, inline=False)
    await ctx.send(embed=embed)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f'Logged in as {bot.user.name}')

@bot.command()
async def hello(ctx):
    await ctx.send('bye')

bot.run(token)