import discord
import asyncio
import os

from dotenv import load_dotenv
from discord.ext import commands, tasks

load_dotenv()

# bot setting
token = os.environ.get("DISSCODE_TOKEN")
prefix = '!'

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

bot.run(token)

