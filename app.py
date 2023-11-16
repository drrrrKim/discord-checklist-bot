import os
import discord 
from dotenv import load_dotenv

from discord.ext import commands
from service import choice_royal, choice_wonki_berry

load_dotenv()
path_dir = os.path.dirname(os.path.realpath(__file__))

# bot setting
token = os.environ.get("DISSCODE_TOKEN")
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

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f'Logged in as {bot.user.name}')

@bot.tree.command(name="원기베리",description="숫자만입력해주세요")
async def 원기베리(interaction:discord.Interaction, 갯수: int):
    if 갯수>25:
        await interaction.response.send_message("25이하의 숫자를 입력")
    else:
        t = await choice_wonki_berry.choice_wonki_berry(path_dir,갯수)
        embed = discord.Embed(
            title="원기베리",
        )
        cnt=0
        for idx in t:
            cnt+=1
            embed.add_field(name=f"{cnt}번째 결과", value=idx, inline=False)

        await interaction.response.send_message(embed=embed)

@bot.tree.command(name="로얄",description="숫자만입력해주세요")
async def 로얄(interaction:discord.Interaction, 갯수: int):
    if 갯수>25:
        await interaction.response.send_message("25이하의 숫자를 입력")
    else:
        t = await choice_royal.choice_royal(path_dir, 갯수)
        embed = discord.Embed(
            title="로얄스타일",
        )
        cnt=0
        for idx in t:
            cnt+=1
            embed.add_field(name=f"{cnt}번째 결과", value=idx, inline=False)

        await interaction.response.send_message(embed=embed)

@bot.command()
async def 좩(ctx):
    checklist_message = await ctx.send(f"재획 List:\n\n{jh} 재획비\n{gc} 경축비\n{mvp} 경뿌 \n{exp} 2배 \n{extreme_gold} 익골\n{vip_exp} vip")
    for emoji in [extreme_gold,gc,jh,mvp,exp,vip_exp ]:
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
        
bot.run(token)