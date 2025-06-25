import pytesseract
import sqlite3
from PIL import Image
from config import DATABASE

def check_payment_slip(img_path):
    # OCR สกัดข้อความจากรูป
    try:
        text = pytesseract.image_to_string(Image.open(img_path), lang="tha+eng")
        # ตัวอย่างเช็คเบื้องต้น
        keywords = ["โอน", "SCB", "ธนาคาร", "พร้อมเพย์", "บาท", "ชื่อบัญชี"]
        found = sum(1 for k in keywords if k in text)
        return found >= 2  # ถ้าเจอคีย์เวิร์ด 2 ขึ้นไป ถือว่า “ผ่าน”
    except Exception as e:
        print("OCR error:", e)
        return False

def update_booking_payment(booking_id, status, slip_path):
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute(
        "UPDATE bookings SET payment_status=?, payment_proof=? WHERE id=?",
        (status, slip_path, booking_id)
    )
    conn.commit()
    conn.close()

def get_all_pending_payments():
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute("SELECT id, payment_proof, payment_status FROM bookings WHERE payment_status='pending'")
    rows = cur.fetchall()
    conn.close()
    return [{"id": r[0], "slip": r[1], "status": r[2]} for r in rows]