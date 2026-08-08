import discord
from discord.ext import commands, tasks
import aiohttp
import xml.etree.ElementTree as ET

class Notifikasi(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channel_notif_id = 1535503408331620355 
        
        # ID Channel YouTube kamu yang sudah benar
        self.yt_channel_id = 'UCODLE_vcAUAquA4u0UKegBQ' 
        
        self.last_yt_video_id = None 
        self.cek_sosmed.start()

    def cog_unload(self):
        self.cek_sosmed.cancel()

    @commands.command()
    async def setnotif(self, ctx):
        self.channel_notif_id = ctx.channel.id
        await ctx.send(f'✅ Channel notifikasi sementara dipindahkan ke {ctx.channel.mention}.')

    # ==========================================
    # COMMAND BARU UNTUK TESTING MANUAL
    # ==========================================
    @commands.command()
    async def testyt(self, ctx):
        await ctx.send("⏳ Sedang menarik data paksa dari YouTube...")
        yt_rss_url = f'https://www.youtube.com/feeds/videos.xml?channel_id={self.yt_channel_id}'
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(yt_rss_url) as respon:
                    if respon.status == 200:
                        teks_xml = await respon.text()
                        root = ET.fromstring(teks_xml)
                        ns = {'yt': 'http://www.w3.org/2005/Atom'}
                        
                        video_terbaru = root.find('yt:entry', ns)
                        if video_terbaru is not None:
                            video_title = video_terbaru.find('yt:title', ns).text
                            video_url = video_terbaru.find('yt:link', ns).attrib['href']
                            
                            pesan = (
                                f"✅ **KONEKSI BERHASIL!**\n"
                                f"Bot berhasil membaca channel YouTube kamu.\n"
                                f"Video teratas yang terdeteksi saat ini:\n**{video_title}**\n{video_url}"
                            )
                            await ctx.send(pesan)
                        else:
                            await ctx.send("⚠️ Terkoneksi ke YouTube, tapi tidak ada video publik yang ditemukan.")
                    else:
                        await ctx.send(f"❌ Gagal koneksi ke YouTube. Error Code: {respon.status}")
        except Exception as e:
            await ctx.send(f"❌ Terjadi error pada sistem: {e}")

    # ==========================================
    # LOGIKA PENGECEKAN OTOMATIS (BACKGROUND)
    # ==========================================
    @tasks.loop(minutes=10)
    async def cek_sosmed(self):
        channel = self.bot.get_channel(self.channel_notif_id)
        if not channel:
            return

        print("Mengecek aktivitas sosmed terbaru...")
        yt_rss_url = f'https://www.youtube.com/feeds/videos.xml?channel_id={self.yt_channel_id}'
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(yt_rss_url) as respon:
                    if respon.status == 200:
                        teks_xml = await respon.text()
                        root = ET.fromstring(teks_xml)
                        
                        ns = {'yt': 'http://www.w3.org/2005/Atom', 'yt_ext': 'http://www.youtube.com/xml/schemas/2015'}
                        video_terbaru = root.find('yt:entry', ns)
                        
                        if video_terbaru is not None:
                            video_id = video_terbaru.find('yt:id', ns).text
                            video_title = video_terbaru.find('yt:title', ns).text
                            video_url = video_terbaru.find('yt:link', ns).attrib['href']
                            
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
                                print(f"Notifikasi terkirim: {video_title}")
        except Exception as e:
            print(f"Gagal mengecek YouTube: {e}")

    @cek_sosmed.before_loop
    async def before_cek(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(Notifikasi(bot))