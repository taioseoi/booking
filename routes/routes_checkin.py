from flask import Blueprint, request, jsonify
import time
import json
import base64

checkin_bp = Blueprint("checkin", __name__)

@checkin_bp.route("/checkin/scan_qr", methods=["POST"])
def scan_qr():
    data = request.json
    qr_data = data.get("qr_data")
    try:
        if not qr_data.startswith("CHECKIN|"):
            return jsonify({"success": False, "msg": "QR ไม่ถูกต้อง"})
        payload_str = qr_data.split("|", 1)[1]
        payload = json.loads(base64.urlsafe_b64decode(payload_str.encode()).decode())
        now = int(time.time())
        if now > payload["expire_at"]:
            return jsonify({"success": False, "msg": "QR นี้หมดอายุแล้ว"})
        booking_id = payload["booking_id"]
        # เพิ่ม logic ตรวจสอบ booking_id ในฐานข้อมูล ว่ามีอยู่จริงและยังไม่ถูก check-in ซ้ำ
        # ตัวอย่าง:
        #   - เช็คว่าจองห้องนี้จริง
        #   - ยังไม่เคย check-in ไปแล้ว
        #   - (option) บันทึกเวลา check-in
        return jsonify({"success": True, "msg": "QR ใช้ได้", "booking_id": booking_id})
    except Exception as e:
        return jsonify({"success": False, "msg": f"QR ไม่ถูกต้อง ({e})"})
    
def verify_expiring_qr(qr_data):
    if not qr_data.startswith("BOOKING|"):
        return False, "QR ไม่ถูกต้อง"
    payload_str = qr_data.split("|", 1)[1]
    try:
        payload = json.loads(base64.urlsafe_b64decode(payload_str.encode()).decode())
        now = int(time.time())
        if now > payload["expire_at"]:
            return False, "QR นี้หมดอายุแล้ว"
        return True, payload  # ใช้ payload เพื่อตรวจสอบ booking_id ฯลฯ ต่อไป
    except Exception as e:
        return False, "QR ไม่ถูกต้อง"