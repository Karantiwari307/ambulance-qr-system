# Ambulance QR System: Project Flow

This document explains the end-to-end architecture and data flow of the Ambulance QR System. It is designed to be a completely cloud-based, zero-maintenance platform where data updates in real-time.

---

## 🏗️ 1. The Core Components

The system is built on three main pillars:
1. **The Database:** A live Google Sheet (`Anyone with the link can view`).
2. **The Server:** A Python Streamlit web application running locally or in the cloud.
3. **The Access Point:** A single, permanent Static QR Code.

---

## 🔄 2. The Data Flow (Step-by-Step)

Here is exactly what happens when a user scans the QR code:

### Step 1: The Scan
- A user points their smartphone camera at the `masterqr.png` QR code.
- The QR code contains a static, hardcoded URL pointing to the Streamlit server (e.g., `http://172.24.90.154:8501/`).
- The user's phone browser opens that URL.

### Step 2: The Server Wakes Up
- The Streamlit web server receives the request from the user's phone.
- Before rendering any visual UI to the user, the server executes `app.services.excelprocessor.py`.

### Step 3: Fetching Live Data (The Magic)
- The server takes the `GOOGLE_SHEET_URL` defined in `config/settings.py`.
- It converts the standard Google Sheet URL into a direct CSV export URL.
- **Cache-Busting:** It attaches a unique millisecond timestamp to the end of the URL (e.g., `&t=1690000000`). This tricks Google's highly-cached Content Delivery Network (CDN) into thinking it's a brand new request, forcing Google to provide the absolute most recent data.
- Using the `pandas` library, the server downloads the live CSV data directly into the server's memory.

### Step 4: Data Processing
- The server drops any completely empty rows or columns to clean the data.
- It verifies that the required columns (`Name`, `Number`, `Type`, `Cost`) exist.
- It iterates through the rows and maps the data into Python dictionaries.

### Step 5: Rendering the UI
- Streamlit takes the processed dictionaries and begins building the HTML/CSS user interface.
- It injects custom Google Fonts (Outfit) and modern CSS styling (glassmorphism cards, dark mode).
- It applies dynamic logic: For example, if an ambulance `Type` contains "ICU", it applies a pulsing red glow animation to that specific card.
- The fully assembled, beautiful UI is sent back over the network to the user's phone.

---

## 🛠️ 3. Why This Architecture is Powerful

### A. Zero QR Code Maintenance
Because the QR code only holds a link to the server (and not the data itself), it never runs out of storage space limit, and it **never needs to be reprinted or regenerated**. 

### B. Instant Live Updates
The Streamlit app acts as a real-time bridge. Whenever a user loads or refreshes the page, the app pulls the newest data from Google Sheets. You can edit the Google Sheet from your laptop, and seconds later, someone scanning the QR code on the street will see your new data.

### C. No Complex Databases
Instead of setting up SQL databases, writing complex backend APIs, or dealing with authentication, the system leverages Google Sheets as a free, highly-scalable, and user-friendly visual database. Anyone who knows how to use Excel can be an administrator for this system.
