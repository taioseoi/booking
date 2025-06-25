import sqlite3
from datetime import datetime, timedelta
from line_utils import push_flex_line
from config import DATABASE
def push_reminder():
    now = datetime.now()
    target_time = now + timedelta(minutes=15)
    target_date_str = target_time.strftime("%Y-%m-%d")
    target_time_str = target_time.strftime("%H:%M")

    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT id, line_user_id, room, date, time FROM bookings WHERE date=? AND time=?", (target_date_str, target_time_str))
    rows = c.fetchall()
    conn.close()

    for booking in rows:
        booking_id, line_user_id, room, date, time = booking
        # คุณควรสร้างฟังก์ชัน build_flex_json เอง หรือ import จากไฟล์อื่น
        flex = {
            "type": "bubble",
            "header": {"type": "box", "layout": "vertical", "contents": [
                {"type": "text", "text": f"แจ้งเตือนห้อง {room}", "weight": "bold"}
            ]},
            "body": {"type": "box", "layout": "vertical", "contents": [
                {"type": "text", "text": f"วันที่: {date}"},
                {"type": "text", "text": f"เวลา: {time}"}
            ]}
        }
        status, resp = push_flex_line(line_user_id, flex)
        print(f"PUSH [{line_user_id}] {room} {date} {time} -> {status} {resp}")