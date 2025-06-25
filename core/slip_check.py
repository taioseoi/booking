import pytesseract
from PIL import Image
import re

def extract_text_from_slip(image_path):
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img, lang='tha+eng')
    return text

def check_slip_valid(text, expected_account, expected_amount):
    # ตรวจหาเลขบัญชี
    account_found = re.search(expected_account, text.replace(' ', ''))
    # ตรวจสอบจำนวนเงิน (เช่น 1,000.00 หรือ 1000.00)
    amount_found = re.search(f'{expected_amount:.2f}', text.replace(',', '').replace(' ', ''))
    return bool(account_found) and bool(amount_found)