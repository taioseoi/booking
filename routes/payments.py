import os
import re
from flask import Blueprint, request, jsonify, render_template, session
from werkzeug.utils import secure_filename
from PIL import Image
import pytesseract

payment_bp = Blueprint('payment', __name__)
UPLOAD_FOLDER = "uploads"
PROMPTPAY_PHONE = "0986619426"  # ปรับเบอร์ promptpay ที่ใช้จริง
# ตัวอย่าง: logic คำนวณยอดเงินจริงควรไปดึงจาก booking_id ที่ user ส่งมา แต่เอาแบบง่ายก่อน
DEFAULT_EXPECTED_AMOUNT = 100

def normalize(text):
    return re.sub(r'\D', '', text or "")

def is_slip_valid(ocr_text, phone, amount):
    norm_text = normalize(ocr_text)
    norm_phone = normalize(phone)[-4:]  # 4 ตัวท้าย
    has_phone = norm_phone in norm_text
    # ตรวจสอบยอดเงิน: ทั้งแบบ 100, 100.00, ๑๐๐, ฯลฯ
    str_amount = str(int(amount))
    has_amount = str_amount in norm_text or "{:.2f}".format(amount).replace('.', '') in norm_text
    return has_phone and has_amount

@payment_bp.route("/upload_slip", methods=["GET", "POST"])
def upload_slip():
    if request.method == "GET":
        booking_id = request.args.get("booking_id")
        if not booking_id:
            return "ไม่พบรหัสการจอง", 400
        return render_template('upload_slip.html', booking_id=booking_id)
    else:  # POST
        booking_id = request.form.get("booking_id")
        file = request.files.get("slip")

        if not file or not booking_id:
            return jsonify({"success": False, "msg": "ข้อมูลไม่ครบ"}), 400

        if not allowed_file(file.filename):
            return jsonify({"success": False, "msg": "ไฟล์ต้องเป็นรูปภาพเท่านั้น"}), 400

        filename = secure_filename(file.filename)
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        save_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(save_path)

        # OCR ด้วย pytesseract
        try:
            img = Image.open(save_path)
            ocr_text = pytesseract.image_to_string(img, lang='tha+eng')
        except Exception as e:
            return jsonify({"success": False, "msg": f"OCR error: {e}"}), 500

        # TODO: ดึงยอดเงินที่ต้องจ่ายจริงจาก booking_id (ตัวอย่างใช้ DEFAULT_EXPECTED_AMOUNT)
        expected_amount = DEFAULT_EXPECTED_AMOUNT

        # ตรวจสอบสลิป
        if is_slip_valid(ocr_text, PROMPTPAY_PHONE, expected_amount):
            # TODO: อัปเดตฐานข้อมูล booking_id นี้เป็น paid, เก็บ path/URL สลิป
            return jsonify({"success": True, "msg": "ตรวจสอบสลิปผ่าน!", "ocr_text": ocr_text})
        else:
            return jsonify({"success": False, "msg": "สลิปไม่ถูกต้อง กรุณาตรวจสอบและอัปโหลดใหม่", "ocr_text": ocr_text}), 400

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'bmp', 'gif'}