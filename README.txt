# Ambulance QR System (Google Sheets Edition)

This system allows you to manage ambulance data centrally in a Google Sheet. Scanning the QR code points users to a Streamlit web app which dynamically reads the Google Sheet and presents a beautiful UI displaying the ambulance details.

## Project Structure
- `app/`: Streamlit app and services (Google Sheets processor, qr generator).
- `config/`: Application settings (Google Sheet URL, Base URL).
- `data/`: Generated QR codes.
- `utils/`: Constants.

## Setup Instructions

1. **Install Requirements:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Google Sheet Setup:**
   - Create a Google Sheet with columns: `Name`, `Number`, `Type`, and `Cost`.
   - Click "Share" in the top right corner.
   - Under "General access", change from "Restricted" to "Anyone with the link".
   - Copy the link.

3. **Configuration:**
   - Open `config/settings.py`.
   - Paste your copied Google Sheet link into the `GOOGLE_SHEET_URL` variable.

4. **Generate QR Code (Only needed once):**
   ```bash
   python -m app.services.qrgenerator
   ```
   This will generate `data/qr/masterqr.png`.

5. **Run Streamlit App:**
   ```bash
   streamlit run app/streamlitapp.py
   ```
   *(Keep this terminal running so your app stays online).*

6. **Usage:**
   Scan `data/qr/masterqr.png` with your phone, or open the URL encoded in it. The Streamlit app will pull the latest data from your Google Sheet and display it! You never need to touch the QR code again.
