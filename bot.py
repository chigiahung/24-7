import os
import asyncio
import discord

# Thay ID phòng Voice của bạn vào đây (Ví dụ: 123456789012345678)
VOICE_CHANNEL_ID = 1211650562148401173  

class VoiceBot(discord.Client):
    def __init__( self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def on_ready(self):
        print(f"Bot {self.user} đã online!")
        
        # Lấy thông tin phòng Voice bằng ID
        channel = self.get_channel(VOICE_CHANNEL_ID)
        
        if channel and isinstance(channel, discord.VoiceChannel):
            try:
                # Tiến hành kết nối vào phòng voice
                vc = await channel.connect()
                print(f" Đã kết nối thành công vào phòng voice: {channel.name}")
                
                # Tùy chọn: Giúp bot tự treo câm/điếc nếu bạn muốn tiết kiệm băng thông
                # await vc.main_mick_status(mute=True, deafen=True) 
                
            except Exception as e:
                print(f"❌ Lỗi khi kết nối vào phòng voice: {e}")
        else:
            print("❌ Không tìm thấy phòng Voice. Hãy kiểm tra lại ID phòng!")

# Khởi tạo bot với Intents cần thiết
intents = discord.Intents.default()
client = VoiceBot(intents=intents)

# Lấy token từ biến môi trường của Wasmer
TOKEN = os.getenv("DISCORD_TOKEN")
client.run(TOKEN)
