from flask import Blueprint, render_template
from core.payments import get_all_pending_payments

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/admin/payments")
def admin_payments():
    payments = get_all_pending_payments()
    return render_template("admin_payments.html", payments=payments)