from datetime import datetime, timedelta, timezone

def now_thai():
    # UTC+7
    return datetime.now(timezone(timedelta(hours=7)))

def format_thai_date(date_str):
    dt = datetime.strptime(date_str, "%Y-%m-%d")
    thai_months = [
        "", "ม.ค.", "ก.พ.", "มี.ค.", "เม.ย.", "พ.ค.", "มิ.ย.",
        "ก.ค.", "ส.ค.", "ก.ย.", "ต.ค.", "พ.ย.", "ธ.ค."
    ]
    day = dt.day
    month = thai_months[dt.month]
    year = dt.year + 543
    return f"{day} {month} {year}"