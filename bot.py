import os
import asyncio
import discord
import datetime
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
ACTIVITY_START_HOURS_AGO = int(os.getenv("ACTIVITY_START_HOURS", "384"))

class VoiceBot(discord.Client):
    async def on_ready(self):
        print(f"🤖 Bot {self.user} đã online thành công!")

        start_time = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=ACTIVITY_START_HOURS_AGO)
        activity = discord.Activity(
            type=discord.ActivityType.listening,
            name="Hung.ai",
            start=start_time
        )
        await self.change_presence(activity=activity)
        print(f"🎵 Đã set activity: Listening to Hung.ai ({ACTIVITY_START_HOURS_AGO}h elapsed)")

        await self.join_voice()

    async def join_voice(self):
        channel = self.get_channel(VOICE_CHANNEL_ID)
        if channel and isinstance(channel, discord.VoiceChannel):
            try:
                if channel.guild.voice_client:
                    await channel.guild.voice_client.disconnect()
                vc = await channel.connect()
                print(f"🔊 Đã nhảy vào phòng voice: {channel.name}")
            except Exception as e:
                print(f"❌ Lỗi kết nối Voice: {e}")
        else:
            print("❌ Không tìm thấy ID phòng Voice hợp lệ!")

    async def on_voice_state_update(self, member, before, after):
        if member == self.user and after.channel is None:
            print("⚠️ Bot bị văng khỏi voice, đang reconnect...")
            await asyncio.sleep(3)
            await self.join_voice()

if __name__ == "__main__":
    web_thread = threading.Thread(target=run_web_server, daemon=True)
    web_thread.start()

    intents = discord.Intents.default()
    intents.voice_states = True
    client = VoiceBot(intents=intents)

    TOKEN = os.getenv("DISCORD_TOKEN")
    client.run(TOKEN)
