import os
import asyncio
import discord
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading

# 1. TẠO WEB SERVER ẢO ĐỂ TRÁNH LỖI VERCEL/WASMER
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write("Bot vẫn đang sống nhăn răng 24/7!".encode("utf-8"))

def run_web_server():
    # Vercel/Wasmer luôn cấp một cổng PORT trong biến môi trường
    port = int(os.getenv("PORT", 8080))
    server = HTTPServer(("0.0.0.0", port), HealthCheckHandler)
    print(f"🌍 Web Server ảo đang chạy tại port: {port}")
    server.serve_forever()

# 2. CẤU HÌNH BOT DISCORD TREO VOICE
VOICE_CHANNEL_ID = 1211650562148401173  # ⚠️ THAY ID PHÒNG VOICE CỦA BẠN VÀO ĐÂY!

class VoiceBot(discord.Client):
    async def on_ready(self):
        print(f"🤖 Bot {self.user} đã online thành công!")
        channel = self.get_channel(VOICE_CHANNEL_ID)
        
        if channel and isinstance(channel, discord.VoiceChannel):
            try:
                vc = await channel.connect()
                print(f"🔊 Đã nhảy vào phòng voice: {channel.name}")
            except Exception as e:
                print(f"❌ Lỗi kết nối Voice: {e}")
        else:
            print("❌ Không tìm thấy ID phòng Voice hợp lệ!")

# 3. KHỞI CHẠY SONG SONG CẢ HAI
if __name__ == "__main__":
    # Chạy Web Server ở một luồng riêng để không làm nghẹt mạng của Bot
    web_thread = threading.Thread(target=run_web_server, daemon=True)
    web_thread.start()

    # Chạy Bot Discord
    intents = discord.Intents.default()
    client = VoiceBot(intents=intents)
    
    TOKEN = os.getenv("DISCORD_TOKEN")
    client.run(TOKEN)
