import time
import json
import base64

def verify_qr(qr_data):
    try:
        if not qr_data.startswith("CHECKIN|"):
            return False, "QR ไม่ถูกต้อง"
        payload_str = qr_data.split("|", 1)[1]
        payload = json.loads(base64.urlsafe_b64decode(payload_str.encode()).decode())
        now = int(time.time())
        if now > payload["expire_at"]:
            return False, "QR นี้หมดอายุแล้ว"
        # สามารถเช็ค booking_id ใน DB เพิ่มเติมได้ที่นี่
        return True, f'QR นี้ใช้ได้ (booking_id={payload["booking_id"]})'
    except Exception as e:
        return False, f'QR ไม่ถูกต้อง ({e})'