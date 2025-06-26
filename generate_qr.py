import datetime
import qrcode
import json
import base64

def generate_booking_qr(booking_id, booking_time):
    # booking_time: datetime.datetime (เช่น 2025-06-26 16:00)
    expire_time = booking_time + datetime.timedelta(minutes=15)
    payload = {
        "booking_id": booking_id,
        "expire_at": int(expire_time.timestamp())
    }
    payload_str = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode()
    qr_data = f"CHECKIN|{payload_str}"
    img = qrcode.make(qr_data)
    img.save(f"qr_{booking_id}.png")
    print(f"สร้าง QR สำหรับ booking_id {booking_id} สำเร็จ (หมดอายุ {expire_time})")
    return qr_data