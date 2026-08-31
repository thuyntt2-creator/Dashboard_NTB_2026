import os
import sys
import gspread
from google.oauth2.service_account import Credentials

# Reconfigure stdout to use UTF-8
try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    pass

JSON_FILE = r'C:\Users\lap4all\Desktop\Backlog_Automation\credentials.json'
creds = Credentials.from_service_account_file(
    JSON_FILE, 
    scopes=['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
)
gc = gspread.authorize(creds)

sheets_to_check = {
    "SHEET_ID (Destination/Report)": "1j6Xm7JRemUGRSfbL-wc8DMwt7qfR7j79w9q79_snVnU",
    "OPS_URL (Source/Operation)": "1DAwY-46twFrHIs77R4p4IMuIZ6JTE-e58Aj-9Kcr5Jk"
}

with open(r"c:\Users\lap4all\Desktop\New folder\scratch\spreadsheet_titles_output.txt", "w", encoding="utf-8") as f:
    for label, sheet_id in sheets_to_check.items():
        try:
            sh = gc.open_by_key(sheet_id)
            f.write(f"\n==========================================\n")
            f.write(f"{label}: '{sh.title}' (ID: {sheet_id})\n")
            f.write(f"==========================================\n")
            f.write("Worksheets:\n")
            for ws in sh.worksheets():
                f.write(f"  - '{ws.title}' (GID: {ws.id})\n")
        except Exception as e:
            f.write(f"Error checking {label} ({sheet_id}): {e}\n")

print("Done writing spreadsheet_titles_output.txt")
