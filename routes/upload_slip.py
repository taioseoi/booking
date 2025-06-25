from flask import Blueprint, request, jsonify
from core.slip_check import extract_text_from_slip, check_slip_valid

upload_bp = Blueprint("upload", __name__)

@upload_bp.route("/upload_slip", methods=["POST"])
def upload_slip():
    file = request.files["slip"]
    # สมมติบันทึกไฟล์ไว้ที่ path นี้
    save_path = f"uploads/{file.filename}"
    file.save(save_path)
    # ข้อมูลที่ควรตรวจสอบ
    expected_account = "1234567890"  # เลขบัญชี
    expected_amount = 1000.00        # จำนวนเงินที่รอ booking
    # OCR
    text = extract_text_from_slip(save_path)
    is_valid = check_slip_valid(text, expected_account, expected_amount)
    if is_valid:
        # อัปเดต booking ในฐานข้อมูลเป็น paid
        # db.update_payment_status(...)
        return jsonify({"success": True, "message": "ตรวจสลิปผ่าน อัปเดตสถานะเรียบร้อย!"})
    else:
        return jsonify({"success": False, "message": "ไม่พบข้อมูลที่ถูกต้องในสลิป กรุณาตรวจสอบอีกครั้ง"})