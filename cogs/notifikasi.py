import discord
from discord.ext import commands, tasks
import scrapetube
import asyncio

class Notifikasi(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channel_notif_id = 1535503408331620355 
        self.yt_channel_id = 'UCODLE_vcAUAquA4u0UKegBQ' 
        self.last_yt_video_id = None 
        
        self.cek_sosmed.start()

    def cog_unload(self):
        self.cek_sosmed.cancel()

    @commands.command()
    async def setnotif(self, ctx):
        self.channel_notif_id = ctx.channel.id
        await ctx.send(f'✅ Channel notifikasi sementara dipindahkan ke {ctx.channel.mention}.')

    # Fungsi jembatan khusus agar proses scraping tidak membuat bot "ngelag"
    def ambil_data_yt(self):
        try:
            # Mengambil 1 video paling baru dari channel
            videos = scrapetube.get_channel(self.yt_channel_id, limit=1)
            return next(videos, None)
        except Exception:
            return None

    # ==========================================
    # COMMAND BARU UNTUK TESTING MANUAL
    # ==========================================
    @commands.command()
    async def testyt(self, ctx):
        await ctx.send("⏳ Menarik data YouTube menggunakan library Scrapetube (Jalur PIP)...")
        
        # Menjalankan scraping di latar belakang
        video_terbaru = await asyncio.to_thread(self.ambil_data_yt)
        
        if video_terbaru:
            video_id = video_terbaru.get('videoId')
            # Scrapetube menyimpan judul di dalam struktur data yang spesifik
            video_title = video_terbaru.get('title', {}).get('runs', [{}])[0].get('text', 'Tanpa Judul')
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            
            pesan = (
                f"✅ **KONEKSI BERHASIL TERTEMBUS!**\n"
                f"Library sukses mengambil data. Video teratas:\n**{video_title}**\n{video_url}"
            )
            await ctx.send(pesan)
        else:
            await ctx.send("❌ Terkoneksi, tapi gagal mendapatkan data video. Pastikan channel tidak kosong.")

    # ==========================================
    # LOGIKA PENGECEKAN OTOMATIS (BACKGROUND)
    # ==========================================
    @tasks.loop(minutes=10)
    async def cek_sosmed(self):
        channel = self.bot.get_channel(self.channel_notif_id)
        if not channel:
            return

        print("Mengecek aktivitas YouTube dengan Scrapetube...")
        video_terbaru = await asyncio.to_thread(self.ambil_data_yt)
        
        if video_terbaru:
            video_id = video_terbaru.get('videoId')
            video_title = video_terbaru.get('title', {}).get('runs', [{}])[0].get('text', 'Tanpa Judul')
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            
            if self.last_yt_video_id is None:
                self.last_yt_video_id = video_id
                print(f"Menyimpan video terakhir: {video_title}")
            elif self.last_yt_video_id != video_id:
                self.last_yt_video_id = video_id
                pesan = (
                    f"📢 **Postingan YouTube Baru!** 📢\n\n"
                    f"**{video_title}**\n"
                    f"Yuk tonton di sini: {video_url}"
                )
                await channel.send(pesan)

    @cek_sosmed.before_loop
    async def before_cek(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(Notifikasi(bot))