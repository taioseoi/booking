import sqlite3

DATABASE = "booking.db"  # หรือ path ฐานข้อมูลจริงของคุณ

conn = sqlite3.connect(DATABASE)
cur = conn.cursor()

# ถ้าอยากลบ booking ทั้งหมด
cur.execute("DELETE FROM bookings")

# หรือถ้าอยากเหลือ booking ล่าสุดอันเดียว (ลบอันอื่นออก)
# cur.execute("DELETE FROM bookings WHERE id NOT IN (SELECT id FROM bookings ORDER BY id DESC LIMIT 1)")

conn.commit()
conn.close()
print("Cleared all bookings (หรือเหลือแค่ booking ล่าสุด) สำเร็จ!")