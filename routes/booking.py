from flask import Blueprint, render_template, session, request, redirect, jsonify, send_file
from core.line_utils import push_flex_line, get_line_auth_url
from core.flex_receipt import build_receipt_flex
from core.utils import format_thai_date
from config import DATABASE, PRICE_PER_ROOM,BASE_URL, generate_expiring_qr_data
import sqlite3
import os
import qrcode
import io
from linebot import LineBotApi
from linebot.models import ImageSendMessage

QR_DIR = os.path.join("static", "qr_images")
booking_bp = Blueprint("booking", __name__)

def save_qr_image(booking_id, qr_data):
    if not os.path.exists(QR_DIR):
        os.makedirs(QR_DIR)
    path = os.path.join(QR_DIR, f"{booking_id}.png")
    img = qrcode.make(qr_data)
    img.save(path)
    return path


def send_qr_to_user(line_user_id, booking_id):
    qr_url = f"{BASE_URL}/static/qr_images/{booking_id}.png"
    access_token = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN", 'fallback-token')
    print("DEBUG: LINE TOKEN", access_token)
    line_bot_api = LineBotApi(access_token)
    image_message = ImageSendMessage(
        original_content_url=qr_url,
        preview_image_url=qr_url
    )
    try:
        line_bot_api.push_message(line_user_id, image_message)
    except Exception as e:
        print("Error sending QR to LINE user:", e)

@booking_bp.route('/datepicker')
def datepicker():
    room = request.args.get("room")
    if not room or room == "None":
        return "กรุณาเข้าผ่านลิงก์ที่ถูกต้อง (room parameter หาย)", 400
    if "line_profile" not in session:
        login_url = get_line_auth_url(room)
        return redirect(login_url)
    return render_template('custom_datepicker.html', room=room, profile=session["line_profile"])

@booking_bp.route("/book", methods=["POST"])
def book():
    print("--- /book called ---")
    print("SESSION:", session)
    try:
        data = request.get_json()
        print("DATA:", data)
        if "line_profile" not in session:
            print("NO line_profile in session")
            return jsonify({"success": False, "msg": "กรุณาเข้าสู่ระบบด้วย LINE"}), 400
        user_id = session["line_profile"]["userId"]
        room = data.get("room")
        if not room or room == "None":
            return jsonify({"success": False, "msg": "ไม่ได้เลือกห้อง"}), 400
        date = data.get("date")
        time = data.get("time")
        print(f"room: {room}, date: {date}, time: {time}")
        if not room or not date or not time:
            print("ข้อมูลไม่ครบ")
            return jsonify({"success": False, "msg": "ข้อมูลไม่ครบ กรุณาเลือกห้อง วัน และเวลา"}), 400

        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute(
            "SELECT * FROM bookings WHERE room=? AND date=? AND time=?",
            (room, date, time)
        )
        if c.fetchone():
            conn.close()
            print("ห้องนี้ถูกจองในวันและเวลาดังกล่าวแล้ว")
            return jsonify({"success": False, "msg": "ห้องนี้ถูกจองในวันและเวลาดังกล่าวแล้ว"}), 400
        c.execute(
            "INSERT INTO bookings (line_user_id, room, date, time, payment_status) VALUES (?, ?, ?, ?, ?)",
            (user_id, room, date, time, 'pending')
        )
        booking_id = c.lastrowid
        conn.commit()
        qr_data = f"BOOKING:{booking_id}|ROOM:{room}|DATE:{date}|TIME:{time}"
        save_qr_image(booking_id, qr_data)
        conn.close()
        


        flex_wait_slip = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {"type": "text", "text": f"จองห้อง {room} สำเร็จ", "weight": "bold", "size": "lg"},
                {"type": "text", "text": "กรุณาอัปโหลดสลิปโอนเงินเพื่อยืนยันการจอง", "wrap": True, "margin": "md"},
            ]
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": [
                {
                    "type": "button",
                    "action": {
                        "type": "uri",
                        "label": "อัปโหลดสลิป",
                        "uri": f"{BASE_URL}/payment/upload_slip?booking_id={booking_id}"
                    },
                    "style": "primary"
                }
            ]
        }
    }
        send_qr_to_user(user_id, booking_id)
        # ไม่ต้อง build_receipt_flex
        push_flex_line(user_id, flex_wait_slip)

        print(f"จองห้อง {room} สำเร็จ! แจ้งรออัปโหลดสลิป")
        return jsonify({"success": True, "msg": f"คุณกำลังจองห้อง {room} สำเร็จ!"})
    except Exception as e:
        print("Exception in /book:", e)
        import traceback; traceback.print_exc()
        return jsonify({"success": False, "msg": "เกิดข้อผิดพลาด (server)"}), 500

@booking_bp.route("/mybookings")
def mybookings():
    print("SESSION:", session)
    if "line_profile" not in session:
        print("NO line_profile in session")
        return jsonify([])
    user_id = session["line_profile"]["userId"]
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute(
        "SELECT id, room, date, time FROM bookings WHERE line_user_id=? ORDER BY date DESC, time DESC",
        (user_id,)
    )
    rows = c.fetchall()
    conn.close()
    bookings = [{"id": r, "room": d, "date": t, "time": u} for r, d, t, u in rows]
    return jsonify(bookings)

@booking_bp.route("/cancel_booking", methods=["POST"])
def cancel_booking():
    try:
        data = request.get_json()
        booking_id = data.get("booking_id")
        if not booking_id:
            return jsonify({"success": False, "msg": "ไม่พบข้อมูล booking_id"}), 400

        if "line_profile" not in session:
            return jsonify({"success": False, "msg": "กรุณาเข้าสู่ระบบ"}), 400
        user_id = session["line_profile"]["userId"]

        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute(
            "SELECT * FROM bookings WHERE id=? AND line_user_id=?",
            (booking_id, user_id)
        )
        booking = c.fetchone()
        if not booking:
            conn.close()
            return jsonify({"success": False, "msg": "ไม่พบข้อมูลการจองนี้"}), 404

        c.execute("DELETE FROM bookings WHERE id=?", (booking_id,))
        conn.commit()
        conn.close()
        return jsonify({"success": True, "msg": "ยกเลิกการจองสำเร็จ"})
    except Exception as e:
        print("Exception in /cancel_booking:", e)
        import traceback; traceback.print_exc()
        return jsonify({"success": False, "msg": "เกิดข้อผิดพลาด (server)"}), 500

@booking_bp.route("/your_booking_page")
def your_booking_page():
    if "line_profile" not in session:
        return redirect(get_line_auth_url())

@booking_bp.route("/get_qr/<int:booking_id>")
def get_qr(booking_id):
    print(f"DEBUG: get_qr called, booking_id={booking_id}")
    print(f"DEBUG: DATABASE PATH = {DATABASE}")
    user_id = request.args.get("user_id")
    print(f"DEBUG: user_id query param = {user_id}")
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT line_user_id, room, date, time, payment_status FROM bookings WHERE id=?", (booking_id,))
    row = c.fetchone()
    print(f"DEBUG: DB select row = {row}")
    conn.close()
    if not row:
        print("DEBUG: Booking not found 404")
        return "ไม่พบ booking", 404
    line_user_id, room, date, time, payment_status = row
    if payment_status != "paid":
        return "ยังไม่ได้ชำระเงิน", 403
    if user_id and user_id != line_user_id:
        return "คุณไม่มีสิทธิ์เข้าถึง QR นี้", 403
    # สร้าง QR code (อาจใส่ข้อมูล booking_id, room, date, time)
    qr_data = generate_expiring_qr_data(booking_id, room, date, time) 
    img = qrcode.make(qr_data)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return send_file(buf, mimetype="image/png")

@booking_bp.route("/get_qr_image/<int:booking_id>")
def get_qr_image(booking_id):
    # ดึงข้อมูล booking เพื่อ encode รายละเอียดเหมือน get_qr
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT room, date, time FROM bookings WHERE id=?", (booking_id,))
    row = c.fetchone()
    conn.close()
    if row:
        room, date, time = row
        qr_data = generate_expiring_qr_data(booking_id, room, date, time)
    else:
        qr_data = f"BOOKING:{booking_id}"
    img = qrcode.make(qr_data)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return send_file(buf, mimetype="image/png")

