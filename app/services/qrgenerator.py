import os
import qrcode
from config.settings import QR_OUTPUT_PATH, BASE_URL

def generate_qr():
    print("Generating Static QR Code...")
    
    final_url = BASE_URL
    print(f"The QR code will permanently point to: {final_url}")
    
    # 4. Generate QR Code
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(final_url)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(QR_OUTPUT_PATH), exist_ok=True)
    
    img.save(QR_OUTPUT_PATH)
    print(f"Success! Static QR code saved to {QR_OUTPUT_PATH}")
    print("You NEVER need to run this script again. Just update the Excel file!")

if __name__ == "__main__":
    generate_qr()
