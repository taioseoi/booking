from flask import Blueprint, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, FlexSendMessage, TextSendMessage, PostbackEvent
from core.flex_utils import build_room_booking_flex, booking_history_flex
from core.flex_receipt import build_receipt_flex
from config import LINE_CHANNEL_ACCESS_TOKEN, LINE_CHANNEL_SECRET, BASE_URL, DATABASE
import sqlite3

linebot_bp = Blueprint("linebot", __name__)
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text.strip().lower()
    line_user_id = event.source.user_id
    print("DEBUG: user_id from LINE OA chat =", line_user_id)

    if "จองห้อง" in user_message:
        rooms = [
            {
                "room": "A101",
                "price": 100,
                "img": "https://www.executivecentre.com/_next/image/?url=%2F_next%2Fstatic%2Fmedia%2FplanOverview-mr-meetingRoom.1f2225da.jpg&w=3840&q=75",
                "size": "Small",
                "url": f"{BASE_URL}/booking/datepicker?room=A101",
                "bg": "#9C8E7Ecc"
            },
            {
                "room": "B202",
                "price": 200,
                "img": "https://patreeda.com/wp-content/uploads/2020/12/cover-nologo-3.jpg",
                "size": "Medium",
                "url": f"{BASE_URL}/booking/datepicker?room=B202",
                "bg": "#1e1e1ecc"
            }
        ]
        flex_msg = build_room_booking_flex(rooms)
        line_bot_api.reply_message(event.reply_token, FlexSendMessage(alt_text="จองห้อง", contents=flex_msg))
        return

    if "ติดต่อ" in user_message:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="คุณสามารถติดต่อผู้ดูแลได้ตลอด 24 ชั่วโมงที่เบอร์ 094-973-2665\n\n ")
        )
        return

    if "ประวัติการจอง" in user_message:
        print("user_id:", line_user_id)
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute("SELECT id, room, date, time FROM bookings WHERE line_user_id=?", (line_user_id,))
        rows = c.fetchall()
        print("DB rows:", rows)
        bookings = [{"id": r, "room": d, "date": t, "time": u} for r, d, t, u in rows]
        conn.close()
        if bookings:
            flex = booking_history_flex(bookings)
            line_bot_api.reply_message(
                event.reply_token,
                FlexSendMessage(alt_text="ประวัติการจองของคุณ", contents=flex)
            )
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="ไม่พบประวัติการจองห้องของคุณ")
            )
        return

    # Default/else case
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(
            text="นี่คือระบบตอบกลับอัตโนมัติ\n\n"
                 "คุณสามารถพิมพ์ จองห้อง เพื่อใช้งานระบบได้\n\n"
                 "หากต้องการติดต่อผู้ดูแลระบบ สามารถพิมพ์ ติดต่อ ได้เลย "
        )
    )

@handler.add(PostbackEvent)
def handle_postback(event):
    data = event.postback.data
    if data.startswith("action=cancel_booking"):
        params = dict(x.split("=") for x in data.split("&"))
        booking_id = params.get("id")
        if not booking_id:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="เกิดข้อผิดพลาด ไม่พบ ID การจอง")
            )
            return
        line_user_id = event.source.user_id
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute("SELECT * FROM bookings WHERE id=? AND line_user_id=?", (booking_id, line_user_id))
        booking = c.fetchone()
        if booking:
            c.execute("DELETE FROM bookings WHERE id=?", (booking_id,))
            conn.commit()
            msg = "ยกเลิกการจองสำเร็จ"
        else:
            msg = "ไม่พบข้อมูลการจองนี้ หรือคุณไม่มีสิทธิ์ยกเลิก"
        conn.close()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=msg)
        )

@linebot_bp.route("/callback", methods=['POST'])
def callback():
    signature = request.headers.get("X-Line-Signature")
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return "OK", 200