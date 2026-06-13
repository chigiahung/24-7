import time
import requests

# 1. PHẢI THÊM CỔNG :8080 VÀO ĐÂY (như bro tự phát hiện lúc nãy á)
URL = "https://ed2a2ef1-bff7-4728-9510-1196555f9c99-00-2fne6g1c4nl3k.spock.replit.dev:8080"
INTERVAL = 2 * 60  # 2 phút

# 2. THÊM HEADER GIẢ LẬP TRÌNH DUYỆT (Né việc Replit thấy bot ping liên tục rồi block)
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

print(f"Bat dau ping bot moi {INTERVAL//60} phut...")

while True:
    try:
        # Gửi request kèm theo cái cổng 8080 và headers
        r = requests.get(URL, headers=HEADERS, timeout=30)
        print(f"[OK] Status: {r.status_code}")
    except Exception as e:
        print(f"[LOI] {e}")
    time.sleep(INTERVAL)
