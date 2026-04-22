import socket
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "localhost"

LOCAL_IP = get_local_ip()
BASE_URL = f"http://{LOCAL_IP}:8501/"

# Retrieve the Google Sheet link from the .env file (so it stays hidden)
GOOGLE_SHEET_URL = os.getenv("GOOGLE_SHEET_URL")

if not GOOGLE_SHEET_URL:
    raise ValueError("GOOGLE_SHEET_URL is missing! Please create a .env file and add your link.")

QR_OUTPUT_PATH = "data/qr/masterqr.png"
