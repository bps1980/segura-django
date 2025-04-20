import pytesseract
from PIL import Image

def extract_text_from_id(image_path):
    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img)
        return text
    except Exception as e:
        return f"OCR failed: {str(e)}"
