import os
import sys
import gspread
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv

sys.stdout.reconfigure(encoding='utf-8')
load_dotenv()

JSON_FILE = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS') or r'C:\Users\lap4all\Desktop\Backlog_Automation\credentials.json'
if not os.path.exists(JSON_FILE):
    JSON_FILE = 'credentials.json'

print("Using JSON credentials file:", JSON_FILE)
if not os.path.exists(JSON_FILE):
    print("Credentials file does not exist!")
    sys.exit(1)

sheet_id = "12VsqpIx1vLOqk6-JKHwgRmdrgu6fxSNPQcpyO0wpvdQ"

try:
    creds = Credentials.from_service_account_file(
        JSON_FILE, 
        scopes=['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
    )
    gc = gspread.authorize(creds)
    sh = gc.open_by_key(sheet_id)
    print("Successfully opened sheet:", sh.title)
    print("Worksheets present:")
    for ws in sh.worksheets():
        print(f" - {ws.title} (ID: {ws.id})")
except Exception as e:
    print(f"Error: {e}")
