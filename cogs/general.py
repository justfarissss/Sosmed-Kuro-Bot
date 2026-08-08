import discord
from discord.ext import commands

# Membuat class Cog untuk kategori General
class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Menggunakan @commands.command() di dalam class
    @commands.command()
    async def tes(self, ctx):
        await ctx.send('Halo! Sistem folder (Cogs) sudah berhasil berjalan.')

    @commands.command()
    async def ping(self, ctx):
        # Contoh command tambahan
        latency = round(self.bot.latency * 1000)
        await ctx.send(f'Pong! Latensi bot: {latency}ms')

# Fungsi wajib untuk mendaftarkan Cog ke dalam bot
async def setup(bot):
    await bot.add_cog(General(bot))