Got it — no emojis, clean, and easy to copy in one go. Here’s a polished, professional README:

---

# Ambulance QR System (Google Sheets Powered)

A simple system to manage ambulance data centrally using Google Sheets and display it dynamically through a Streamlit web application.

A single QR code is used. When scanned, it opens a web app that always shows the latest ambulance data. No need to regenerate QR codes after updates.

---

## Overview

This project connects a Google Sheet (as a database) with a Streamlit frontend. The QR code contains a URL that points to the app, which fetches and displays live data.

---

## Key Features

* Single QR code for all ambulance data
* Real-time updates via Google Sheets
* No need to regenerate QR codes
* Simple and modular architecture
* Mobile-friendly interface

---

## Project Structure

```
project-root/

├── app/
│   ├── streamlitapp.py
│   └── services/
│       ├── qrgenerator.py
│       └── sheets_processor.py
│
├── config/
│   └── settings.py
│
├── data/
│   └── qr/
│       └── masterqr.png
│
├── utils/
│   └── constants.py
│
├── requirements.txt
└── README.md
```

---

## Setup Instructions

### 1. Install Dependencies

```
pip install -r requirements.txt
```

---

### 2. Google Sheet Setup

Create a Google Sheet with the following columns:

```
Name | Number | Type | Cost
```

Then:

1. Click "Share"
2. Change access from "Restricted" to "Anyone with the link"
3. Copy the Google Sheet URL

---

### 3. Configuration

Open:

```
config/settings.py
```

Update:

```
GOOGLE_SHEET_URL = "your_google_sheet_link_here"
```

---

### 4. Generate QR Code (One-Time Step)

```
python -m app.services.qrgenerator
```

This generates:

```
data/qr/masterqr.png
```

This QR code does not need to be regenerated after data changes.

---

### 5. Run the Application

```
streamlit run app/streamlitapp.py
```

Keep the terminal running while using the app.

---

## Usage

Scan the QR code:

```
data/qr/masterqr.png
```

Or open the encoded URL directly.

The app will fetch the latest data from Google Sheets and display all ambulance details.

---

## How It Works

1. QR code contains a URL
2. User scans the QR code
3. Streamlit app opens
4. App fetches live data from Google Sheets
5. Data is displayed in the UI





