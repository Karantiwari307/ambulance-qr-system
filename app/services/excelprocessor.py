import pandas as pd
from utils.constants import KEY_MAPPING

def process_sheet(sheet_url):
    """
    Reads the Google Sheet directly from the internet, drops empty rows/cols, 
    and converts it to a list of dictionaries with shortened keys.
    """
    try:
        import re
        import time
        # Extract the Document ID using regex to be completely bulletproof
        match = re.search(r'/d/([a-zA-Z0-9-_]+)', sheet_url)
        if not match:
            raise ValueError("Invalid Google Sheets URL format")
            
        doc_id = match.group(1)
        # Add a timestamp to bypass Google's aggressive caching of the export URL
        timestamp = int(time.time())
        csv_export_url = f"https://docs.google.com/spreadsheets/d/{doc_id}/export?format=csv&t={timestamp}"
        
        # Read the sheet directly as CSV
        df = pd.read_csv(csv_export_url)
        
        # Clean data: drop completely empty rows and columns
        df = df.dropna(how='all').dropna(axis=1, how='all')
        
        # Strip whitespace from columns to prevent matching errors
        df.columns = df.columns.str.strip()
        print("DEBUG COLUMNS:", df.columns.tolist())
        
        # Validate columns
        required_cols = ["Name", "Number", "Type", "Cost"]
        for col in required_cols:
            if col not in df.columns:
                raise ValueError(f"Missing required column: {col}")
        
        # Convert to dictionary format
        records = df.to_dict(orient='records')
        
        processed_data = []
        for record in records:
            # Skip if any of the required fields are NA
            if pd.isna(record.get("Name")) or pd.isna(record.get("Number")):
                continue
                
            short_record = {}
            for full_key, short_key in KEY_MAPPING.items():
                val = record.get(full_key, "")
                if pd.isna(val):
                    val = ""
                # Convert numbers to string to prevent float representation
                short_record[short_key] = str(val).strip()
                # Remove decimal .0 if it's a number parsed as float
                if short_record[short_key].endswith('.0'):
                    short_record[short_key] = short_record[short_key][:-2]
            
            processed_data.append(short_record)
            
        return processed_data
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Error reading from Google Sheet: {e}")
        return None
