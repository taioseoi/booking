from flask import Blueprint, request, jsonify
from core.slip_ai_check import predict_slip
import os

ai_upload_bp = Blueprint("ai_upload", __name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@ai_upload_bp.route("/upload_slip_ai", methods=["POST"])
def upload_slip_ai():
    file = request.files.get("slip")
    if not file:
        return jsonify({"success": False, "msg": "ไม่พบไฟล์สลิป"}), 400
    filename = file.filename
    save_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(save_path)
    try:
        pred, prob = predict_slip(save_path)
    except Exception as e:
        return jsonify({"success": False, "msg": f"ทำนายสลิปไม่สำเร็จ: {e}"}), 500
    if pred == "real_slips" and prob > 0.8:
        return jsonify({"success": True, "ai_result": "ผ่าน", "score": prob})
    else:
        return jsonify({"success": False, "ai_result": "อาจเป็นสลิปปลอม", "score": prob})