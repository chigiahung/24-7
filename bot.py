import os
import asyncio
import discord
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading

class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write("Bot vẫn đang sống nhăn răng 24/7!".encode("utf-8"))

    def log_message(self, format, *args):
        pass

def run_web_server():
    port = int(os.getenv("PORT", 8080))
    server = HTTPServer(("0.0.0.0", port), HealthCheckHandler)
    print(f"🌍 Web Server ảo đang chạy tại port: {port}")
    server.serve_forever()

VOICE_CHANNEL_ID = int(os.getenv("VOICE_CHANNEL_ID", "0"))

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

if __name__ == "__main__":
    web_thread = threading.Thread(target=run_web_server, daemon=True)
    web_thread.start()

    intents = discord.Intents.default()
    client = VoiceBot(intents=intents)

    TOKEN = os.getenv("DISCORD_TOKEN")
    client.run(TOKEN)
