@app.route("/test_push")
def test_push():
    user_id = "U2aad7860092b75cbd0faf218b516b644"  # เปลี่ยนเป็น userId ที่จะทดสอบ
    push_flex_line(user_id, flex_json)
    return "Pushed!"