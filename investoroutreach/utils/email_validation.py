import os
import requests
from dotenv import load_dotenv

load_dotenv()

ZEROBOUNCE_API_KEY = os.getenv("ZEROBOUNCE_API_KEY")

def validate_email_zerobounce(email):
    url = "https://api.zerobounce.net/v2/validate"
    params = {
        "api_key": ZEROBOUNCE_API_KEY,
        "email": email
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        result = response.json()
        return result  # {'status': 'valid', 'email': ..., ...}
    except Exception as e:
        return {"status": "unknown", "error": str(e)}
