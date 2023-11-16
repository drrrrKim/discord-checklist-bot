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


bot.run(token)