from datetime import datetime, timedelta, timezone
import json
import base64

def now_thai():
    # UTC+7
    return datetime.now(timezone(timedelta(hours=7)))

def format_thai_date(date_str):
    dt = datetime.strptime(date_str, "%Y-%m-%d")
    thai_months = [
        "", "ม.ค.", "ก.พ.", "มี.ค.", "เม.ย.", "พ.ค.", "มิ.ย.",
        "ก.ค.", "ส.ค.", "ก.ย.", "ต.ค.", "พ.ย.", "ธ.ค."
    ]
    day = dt.day
    month = thai_months[dt.month]
    year = dt.year + 543
    return f"{day} {month} {year}"


def generate_expiring_qr_data(booking_id, room, date, time):
    # Convert date+time string to datetime object (สมมติ date = "2025-06-26", time = "16:00-18:00")
    book_start = f"{date} {time.split('-')[0]}"
    dt = datetime.datetime.strptime(book_start, "%Y-%m-%d %H:%M")
    expire_time = dt + datetime.timedelta(minutes=15)
    payload = {
        "booking_id": booking_id,
        "room": room,
        "date": date,
        "time": time,
        "expire_at": int(expire_time.timestamp())
    }
    payload_str = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode()
    return f"BOOKING|{payload_str}"