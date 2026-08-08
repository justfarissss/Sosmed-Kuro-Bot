import discord
from discord.ext import commands, tasks
import aiohttp

class Notifikasi(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Memasukkan ID channel secara langsung
        self.channel_notif_id = 1535503408331620355 
        
        # Mulai menjalankan tugas pengecekan otomatis
        self.cek_sosmed.start()

    # Mematikan tugas jika Cog di-reload/dimatikan
    def cog_unload(self):
        self.cek_sosmed.cancel()

    # (Opsional) Command setnotif tetap dibiarkan jika suatu saat 
    # kamu ingin memindahkan notifikasi ke channel lain tanpa mengubah kode
    @commands.command()
    async def setnotif(self, ctx):
        self.channel_notif_id = ctx.channel.id
        await ctx.send(f'✅ Channel notifikasi sementara dipindahkan ke {ctx.channel.mention}.')

    # Tugas latar belakang yang berjalan setiap 10 menit
    @tasks.loop(minutes=10)
    async def cek_sosmed(self):
        # Mengambil objek channel berdasarkan ID
        channel = self.bot.get_channel(self.channel_notif_id)
        
        if not channel:
            print(f"Channel dengan ID {self.channel_notif_id} tidak ditemukan.")
            return

        print(f"Sedang mengecek sosmed... Notifikasi akan dikirim ke channel: {channel.name}")
        
        # ==========================================
        # LOGIKA PENGECEKAN SOSMED DI SINI
        # ==========================================
        # (Nanti kita tambahkan kode scraping/API-nya di sini)

    # Pastikan bot sudah menyala sepenuhnya sebelum mulai mengecek
    @cek_sosmed.before_loop
    async def before_cek(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(Notifikasi(bot))