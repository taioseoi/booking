def build_receipt_flex(room, date, time, price, booking_id):
    return {
      "type": "bubble",
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {"type": "text", "text": "RECEIPT", "weight": "bold", "color": "#1DB446", "size": "sm"},
          {"type": "text", "text": "Booking Room", "weight": "bold", "size": "xxl", "margin": "md"},
          {"type": "text", "text": "ใบเสร็จจองห้องประชุม", "size": "xs", "color": "#aaaaaa", "wrap": True},
          {"type": "separator", "margin": "xxl"},
          {
            "type": "box",
            "layout": "vertical",
            "margin": "xxl",
            "spacing": "sm",
            "contents": [
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {"type": "text", "text": "ห้อง", "size": "sm", "color": "#555555", "flex": 0},
                  {"type": "text", "text": room, "size": "sm", "color": "#111111", "align": "end"}
                ]
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {"type": "text", "text": "วันที่", "size": "sm", "color": "#555555", "flex": 0},
                  {"type": "text", "text": date, "size": "sm", "color": "#111111", "align": "end"}
                ]
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {"type": "text", "text": "เวลา", "size": "sm", "color": "#555555", "flex": 0},
                  {"type": "text", "text": time, "size": "sm", "color": "#111111", "align": "end"}
                ]
              },
              {"type": "separator", "margin": "xxl"},
              {
                "type": "box",
                "layout": "horizontal",
                "margin": "xxl",
                "contents": [
                  {"type": "text", "text": "ราคารวม", "size": "sm", "color": "#555555"},
                  {"type": "text", "text": f"{price:.2f} บาท", "size": "sm", "color": "#111111", "align": "end"}
                ]
              }
            ]
          },
          {"type": "separator", "margin": "xxl"},
          {
            "type": "box",
            "layout": "horizontal",
            "margin": "md",
            "contents": [
              {"type": "text", "text": "BOOKING ID", "size": "xs", "color": "#aaaaaa", "flex": 0},
              {"type": "text", "text": f"#{booking_id}", "color": "#aaaaaa", "size": "xs", "align": "end"}
            ]
          }
        ]
      },
      "styles": {
        "footer": {
          "separator": True
        }
      }
    }


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