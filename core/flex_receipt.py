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