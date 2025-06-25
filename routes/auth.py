from flask import Blueprint, render_template, redirect, url_for, session, request
from core.line_utils import get_line_auth_url
from config import LINE_REDIRECT_URI, LINE_CLIENT_ID, LINE_CLIENT_SECRET  # <--- แนะนำ
import requests

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/")
def index():
    line_login_url = get_line_auth_url()
    return render_template("login.html", line_login_url=line_login_url)

@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.index"))

@auth_bp.route("/line_login_callback")
def line_login_callback():
    code = request.args.get("code")
    state = request.args.get("state") or ""
    room = None
    if state.startswith("ROOM_"):
        room = state[5:]
    if not code:
        return "Missing LINE login code", 400
    token_res = requests.post(
        "https://api.line.me/oauth2/v2.1/token",
        headers={'Content-Type': 'application/x-www-form-urlencoded'},
        data={
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": LINE_REDIRECT_URI,
            "client_id": LINE_CLIENT_ID,
            "client_secret": LINE_CLIENT_SECRET
        }
    )
    if token_res.status_code != 200:
        return "LINE token exchange failed: " + token_res.text, 400

    access_token = token_res.json().get("access_token")
    if not access_token:
        return "No access token from LINE", 400

    userinfo = requests.get(
        "https://api.line.me/v2/profile",
        headers={"Authorization": f"Bearer {access_token}"}
    ).json()
    session["line_profile"] = userinfo
    return redirect(url_for("booking.datepicker", room=room) if room else url_for("booking.datepicker"))