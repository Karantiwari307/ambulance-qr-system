import streamlit as st
import os

# Add app directory to path so services can be imported correctly
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.services.excelprocessor import process_sheet
from config.settings import GOOGLE_SHEET_URL

def inject_custom_css():
    st.markdown("""
        <style>
        /* Import Google Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');
        
        /* Global Styles */
        html, body, [class*="css"]  {
            font-family: 'Outfit', sans-serif;
        }
        
        .stApp {
            background-color: #0d1117;
            color: #c9d1d9;
        }

        /* Header Styles */
        .main-header {
            text-align: center;
            background: linear-gradient(135deg, #ff4b4b 0%, #ff8f00 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 3rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
            animation: fadeIn 1.5s ease-in-out;
        }
        .sub-header {
            text-align: center;
            color: #8b949e;
            margin-bottom: 3rem;
            font-size: 1.2rem;
            font-weight: 300;
        }

        /* Card Layout */
        .ambulance-card {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 16px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            transition: all 0.3s ease;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
            backdrop-filter: blur(10px);
        }
        
        .ambulance-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 20px rgba(0, 0, 0, 0.4);
            border-color: rgba(255, 75, 75, 0.4);
        }
        
        .icu-card {
            background: linear-gradient(145deg, rgba(255,75,75,0.05) 0%, rgba(255,75,75,0.15) 100%);
            border: 1px solid rgba(255, 75, 75, 0.3);
        }

        /* Card Content */
        .card-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid rgba(255,255,255,0.1);
            padding-bottom: 0.5rem;
            margin-bottom: 0.5rem;
        }
        
        .amb-name {
            font-size: 1.4rem;
            font-weight: 600;
            color: #ffffff;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        
        .amb-type {
            padding: 0.25rem 0.75rem;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .type-normal {
            background: rgba(88, 166, 255, 0.2);
            color: #58a6ff;
        }
        
        .type-icu {
            background: rgba(255, 123, 114, 0.2);
            color: #ff7b72;
            animation: pulse 2s infinite;
        }

        .card-details {
            display: flex;
            flex-direction: column;
            gap: 0.75rem;
            margin-top: 0.5rem;
        }

        .detail-row {
            display: flex;
            align-items: center;
            gap: 1rem;
        }

        .detail-icon {
            font-size: 1.2rem;
            width: 30px;
            text-align: center;
        }

        .detail-text {
            font-size: 1.1rem;
            color: #c9d1d9;
        }
        
        .cost-text {
            font-weight: 600;
            color: #3fb950;
        }

        /* Animations */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(-20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        @keyframes pulse {
            0% { box-shadow: 0 0 0 0 rgba(255, 123, 114, 0.4); }
            70% { box-shadow: 0 0 0 6px rgba(255, 123, 114, 0); }
            100% { box-shadow: 0 0 0 0 rgba(255, 123, 114, 0); }
        }

        /* Empty State */
        .empty-state {
            text-align: center;
            padding: 4rem 2rem;
            background: rgba(255, 255, 255, 0.02);
            border-radius: 16px;
            border: 1px dashed rgba(255, 255, 255, 0.2);
            margin-top: 2rem;
        }
        
        .empty-icon {
            font-size: 4rem;
            margin-bottom: 1rem;
            opacity: 0.5;
        }
        
        .empty-text {
            font-size: 1.2rem;
            color: #8b949e;
        }
        </style>
    """, unsafe_allow_html=True)

def main():
    st.set_page_config(
        page_title="Emergency Ambulance Services",
        page_icon="🚑",
        layout="centered",
        initial_sidebar_state="collapsed"
    )
    
    inject_custom_css()
    
    st.markdown("<h1 class='main-header'>Ambulance Services Available</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-header'>Scan the QR code to instantly view and contact emergency vehicles near you.</p>", unsafe_allow_html=True)
    
    try:
        from utils.constants import REVERSE_KEY_MAPPING
        
        # Directly read and process from Google Sheets
        raw_data = process_sheet(GOOGLE_SHEET_URL)
        
        if raw_data is None:
            st.markdown("""
                <div class='empty-state'>
                    <div class='empty-icon'>⚠️</div>
                    <h3 style='color: #ffffff;'>Connection Error</h3>
                    <p class='empty-text'>Could not connect to the Google Sheet. Please check the URL and permissions.</p>
                </div>
            """, unsafe_allow_html=True)
            return
        
        if not raw_data or len(raw_data) == 0:
            st.markdown("""
                <div class='empty-state'>
                    <div class='empty-icon'>📱</div>
                    <h3 style='color: #ffffff;'>No Ambulances Available</h3>
                    <p class='empty-text'>The ambulance database is currently empty.</p>
                </div>
            """, unsafe_allow_html=True)
            return
            
        # Display the data
        st.write(f"Live Status: {len(raw_data)} ambulances available.")
        
        for record in raw_data:
            # Reconstruct the full keys from the short keys provided by process_excel
            amb = {}
            for short_key, val in record.items():
                full_key = REVERSE_KEY_MAPPING.get(short_key, short_key)
                amb[full_key] = val

            name = amb.get("Name", "Unknown")
            number = amb.get("Number", "N/A")
            type_val = amb.get("Type", "Normal")
            cost = amb.get("Cost", "Variable")
            
            # Determine card style based on type
            is_icu = "icu" in str(type_val).lower()
            card_class = "ambulance-card icu-card" if is_icu else "ambulance-card"
            type_class = "amb-type type-icu" if is_icu else "amb-type type-normal"
            
            card_html = f"""
            <div class='{card_class}'>
                <div class='card-header'>
                    <div class='amb-name'>🚑 {name}</div>
                    <div class='{type_class}'>{type_val}</div>
                </div>
                <div class='card-details'>
                    <div class='detail-row'>
                        <div class='detail-icon'>📞</div>
                        <div class='detail-text'>{number}</div>
                    </div>
                    <div class='detail-row'>
                        <div class='detail-icon'>💰</div>
                        <div class='detail-text cost-text'>₹{cost}</div>
                    </div>
                </div>
            </div>
            """
            st.markdown(card_html, unsafe_allow_html=True)
            
    except Exception as e:
        st.error(f"An error occurred while reading the data: {e}")

if __name__ == "__main__":
    main()
