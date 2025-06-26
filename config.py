import os

# Flask secret key
SECRET_KEY = os.environ.get("SECRET_KEY", "default-very-secret-key")

# LINE Login/LINE OA
LINE_CLIENT_ID = os.environ.get("LINE_CLIENT_ID", "")
LINE_CLIENT_SECRET = os.environ.get("LINE_CLIENT_SECRET", "")
LINE_REDIRECT_URI = os.environ.get("LINE_REDIRECT_URI", "")

LINE_CHANNEL_ACCESS_TOKEN = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN", "")
LINE_CHANNEL_SECRET = os.environ.get("LINE_CHANNEL_SECRET", "")

BASE_URL = os.environ.get("BASE_URL", "")

# Database
DATABASE = os.environ.get("DATABASE", "booking.db")

# ราคาห้อง (ตัวอย่าง: ใช้ ENV เป็น JSON string)
import json
PRICE_PER_ROOM = json.loads(os.environ.get("PRICE_PER_ROOM", '{"A101": 100, "B202": 200}'))

