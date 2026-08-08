import discord
import os
import asyncio
from discord.ext import commands
from dotenv import load_dotenv

# Memuat variabel dari .env
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
# Mengambil prefix dari .env (jika tidak ada, otomatis pakai '!')
PREFIX = os.getenv('PREFIX', '!')

intents = discord.Intents.default()
intents.message_content = True

# Modifikasi: Bot merespon saat di-mention ATAU menggunakan prefix dari .env
bot = commands.Bot(command_prefix=commands.when_mentioned_or(PREFIX), intents=intents)

async def load_cogs():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')
            print(f'Berhasil memuat cog: {filename}')

@bot.event
async def on_ready():
    print(f'Bot berhasil login sebagai {bot.user}')
    print(f'Prefix yang digunakan: {PREFIX}')
    print('--- Sistem Siap ---')

async def main():
    async with bot:
        await load_cogs()
        await bot.start(TOKEN)

if __name__ == '__main__':
    asyncio.run(main())