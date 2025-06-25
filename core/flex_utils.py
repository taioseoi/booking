def booking_history_flex(bookings):
    """
    สร้าง Flex Message Carousel สำหรับประวัติการจองห้อง
    """
    bubbles = []
    for b in bookings:
        bubbles.append({
            "type": "bubble",
            "hero": {
                "type": "image",
                "url": "https://www.executivecentre.com/_next/image/?url=%2F_next%2Fstatic%2Fmedia%2FplanOverview-mr-meetingRoom.1f2225da.jpg&w=3840&q=75",
                "size": "full",
                "aspectRatio": "20:13",
                "aspectMode": "cover"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "spacing": "md",
                "contents": [
                    {
                        "type": "text",
                        "text": "Booking Confirmation",
                        "wrap": True,
                        "weight": "bold",
                        "gravity": "center",
                        "size": "xl"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "margin": "lg",
                        "spacing": "sm",
                        "contents": [
                            {
                                "type": "box",
                                "layout": "baseline",
                                "spacing": "sm",
                                "contents": [
                                    {"type": "text", "text": "Date", "color": "#aaaaaa", "size": "sm", "flex": 1},
                                    {"type": "text", "text": b["date"] + " " + b["time"], "wrap": True, "size": "sm", "color": "#666666", "flex": 4}
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "baseline",
                                "spacing": "sm",
                                "contents": [
                                    {"type": "text", "text": "Room", "color": "#aaaaaa", "size": "sm", "flex": 1},
                                    {"type": "text", "text": b["room"], "wrap": True, "color": "#666666", "size": "sm", "flex": 4}
                                ]
                            }
                        ]
                    }
                ]
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "spacing": "sm",
                "contents": [
                    {
                        "type": "button",
                        "style": "primary",
                        "color": "#e57373",
                        "action": {
                            "type": "postback",
                            "label": "ยกเลิกการจอง",
                            "data": f"action=cancel_booking&id={b['id']}"
                        }
                    }
                ]
            }
        })
    return {
        "type": "carousel",
        "contents": bubbles
    }

def build_room_booking_flex(rooms):
    """
    สร้าง Flex Message Carousel สำหรับจองห้องแบบ dynamic
    """
    bubbles = []
    for r in rooms:
        bubble = {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {"type": "image", "url": r['img'], "size": "full", "aspectMode": "cover", "aspectRatio": "2:3", "gravity": "top"},
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {"type": "text", "text": r['room'], "size": "xl", "color": "#ffffff", "weight": "bold"}
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "baseline",
                                "contents": [
                                    {"type": "text", "text": f"{r['price']}฿/ชั่วโมง", "color": "#ebebeb", "size": "sm", "flex": 0}
                                ],
                                "spacing": "lg"
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {"type": "filler"},
                                    {
                                        "type": "box",
                                        "layout": "baseline",
                                        "contents": [
                                            {"type": "filler"},
                                            {"type": "icon", "url": "https://i.ibb.co/SDyfwwJj/booking-1.png"},
                                            {
                                                "type": "text",
                                                "text": "จองห้องนี้",
                                                "color": "#ffffff",
                                                "flex": 0,
                                                "offsetTop": "-2px",
                                                "action": {
                                                    "type": "uri",
                                                    "label": "จองห้องนี้",
                                                    "uri": r['url']
                                                }
                                            },
                                            {"type": "filler"}
                                        ],
                                        "spacing": "sm"
                                    },
                                    {"type": "filler"}
                                ],
                                "borderWidth": "1px",
                                "cornerRadius": "4px",
                                "spacing": "sm",
                                "borderColor": "#ffffff",
                                "margin": "xxl",
                                "height": "40px"
                            }
                        ],
                        "position": "absolute",
                        "offsetBottom": "0px",
                        "offsetStart": "0px",
                        "offsetEnd": "0px",
                        "backgroundColor": r.get('bg', "#9C8E7Ecc"),
                        "paddingAll": "20px",
                        "paddingTop": "18px"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": r.get('size', ''),
                                "color": "#ffffff",
                                "align": "center",
                                "size": "xs",
                                "offsetTop": "xs",
                                "action": {
                                    "type": "datetimepicker",
                                    "label": "action",
                                    "data": "hello",
                                    "mode": "date"
                                }
                            }
                        ],
                        "position": "absolute",
                        "cornerRadius": "20px",
                        "offsetTop": "18px",
                        "backgroundColor": "#ff334b",
                        "offsetStart": "18px",
                        "height": "25px",
                        "width": "53px"
                    }
                ],
                "paddingAll": "0px"
            }
        }
        bubbles.append(bubble)
    return {"type": "carousel", "contents": bubbles}