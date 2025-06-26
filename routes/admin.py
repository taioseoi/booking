from flask import Blueprint, render_template

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin/dashboard')
def admin_dashboard():
    return render_template('admin_dashboard.html')

# เพิ่ม API endpoint ที่จะใช้กับ Chart.js และตาราง
@admin_bp.route('/admin/dashboard_data')
def admin_dashboard_data():
    # สร้าง dict ข้อมูลตามตัวอย่าง JSON ที่ตอบกลับ (Mock หรือ Query จาก DB)
    return {
        "totalBookings": 20,
        "totalPaid": 10000,
        "pendingCount": 4,
        "perMonth": [
            {"month": "2025-05", "count": 8, "sumPaid": 4000},
            {"month": "2025-06", "count": 12, "sumPaid": 6000}
        ],
        "allBookings": [
            {
                "room": "A101",
                "date": "2025-06-26",
                "time": "10:00-12:00",
                "user": "สมชาย",
                "status": "ชำระแล้ว",
                "amount": 500
            }
        ]
    }