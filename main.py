from dotenv import load_dotenv
import os

load_dotenv()
import discord
from discord.ext import commands
import database
import asyncio

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

@bot.event
async def on_ready():
    database.criar_tabelas()
    print(f"Vigil online como {bot.user}")

async def main():
    async with bot:
        await bot.load_extension("commands.keywords")
        await bot.load_extension("commands.channels")
        await bot.load_extension("commands.config")
        await bot.load_extension("events.monitor")
        await bot.start(os.getenv("TOKEN"))

asyncio.run(main())