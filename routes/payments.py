import os
import re
import sqlite3
from flask import Blueprint, request, jsonify, render_template
from werkzeug.utils import secure_filename
from PIL import Image
import pytesseract

payment_bp = Blueprint('payment', __name__)
UPLOAD_FOLDER = "uploads"
PROMPTPAY_PHONE = "0986619426"
DATABASE = "booking.db"

def normalize(text):
    th_digits = "๐๑๒๓๔๕๖๗๘๙"
    ar_digits = "0123456789"
    text = text or ""
    for i, th in enumerate(th_digits):
        text = text.replace(th, ar_digits[i])
    return re.sub(r'\D', '', text)

def get_booking_amount_and_path(booking_id):
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    # ถ้าไม่มี column amount/payment_proof ให้ลบหรือคอมเมนต์ field เหล่านี้
    cur.execute("SELECT amount, payment_proof FROM bookings WHERE id=?", (booking_id,))
    row = cur.fetchone()
    conn.close()
    if row:
        return row[0], row[1]
    return None, None

def update_booking_payment(booking_id, status, slip_path):
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute(
        "UPDATE bookings SET payment_status=?, payment_proof=? WHERE id=?",
        (status, slip_path, booking_id)
    )
    conn.commit()
    conn.close()

def is_slip_valid(ocr_text, phone, amount):
    norm_text = normalize(ocr_text)
    norm_phone = normalize(phone)[-4:]
    has_phone = norm_phone in norm_text
    if amount:  # ถ้ามี column amount
        str_amount = str(int(amount))
        has_amount = str_amount in norm_text or "{:.2f}".format(amount).replace('.', '') in norm_text
        return has_phone and has_amount
    else:
        return has_phone

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'bmp', 'gif'}

@payment_bp.route("/upload_slip", methods=["GET", "POST"])
def upload_slip():
    if request.method == "GET":
        booking_id = request.args.get("booking_id")
        if not booking_id:
            return "ไม่พบรหัสการจอง", 400
        return render_template('upload_slip.html', booking_id=booking_id)
    else:
        booking_id = request.form.get("booking_id")
        file = request.files.get("slip")

        if not file or not booking_id:
            return jsonify({"success": False, "msg": "ข้อมูลไม่ครบ"}), 400

        if not allowed_file(file.filename):
            return jsonify({"success": False, "msg": "ไฟล์ต้องเป็นรูปภาพเท่านั้น"}), 400

        filename = secure_filename(file.filename)
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        save_path = os.path.join(UPLOAD_FOLDER, f"{booking_id}_{filename}")
        file.save(save_path)

        amount, old_slip = get_booking_amount_and_path(booking_id)
        # ถ้าไม่มี amount (กรณี schema เดิม) ให้ข้าม validation ยอด
        # หรือกำหนด amount เป็น None ก็ได้
        # ถ้าไม่มี column amount ให้ใช้ amount = None

        # OCR
        try:
            img = Image.open(save_path)
            ocr_text = pytesseract.image_to_string(img, lang='tha+eng')
        except Exception as e:
            return jsonify({"success": False, "msg": f"OCR error: {e}"}), 500

        if is_slip_valid(ocr_text, PROMPTPAY_PHONE, amount):
            update_booking_payment(booking_id, 'paid', save_path)
            return jsonify({"success": True, "msg": "ตรวจสอบสลิปผ่าน อัปเดตสถานะเรียบร้อย!", "ocr_text": ocr_text})
        else:
            return jsonify({"success": False, "msg": "สลิปไม่ถูกต้อง กรุณาตรวจสอบและอัปโหลดใหม่", "ocr_text": ocr_text}), 400