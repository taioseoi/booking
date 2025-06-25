from flask import Blueprint, request, jsonify, session, render_template
from werkzeug.utils import secure_filename
import os
from core.payments import check_payment_slip, update_booking_payment

payment_bp = Blueprint("payment", __name__)

UPLOAD_FOLDER = "static/payment_slips"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and '.' in filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
            return jsonify({"success": False, "msg": "ข้อมูลไม่ครบ"})

        if not allowed_file(file.filename):
            return jsonify({"success": False, "msg": "ไฟล์ต้องเป็นรูปภาพเท่านั้น"})

        filename = secure_filename(file.filename)
        save_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(save_path)

        # ตรวจสอบสลิป
        result = check_payment_slip(save_path)
        status = "verified" if result else "rejected"

        # อัปเดตฐานข้อมูล
        update_booking_payment(booking_id, status, save_path)

        return jsonify({"success": True, "status": status})