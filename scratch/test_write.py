import gspread
from google.oauth2.service_account import Credentials
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

JSON_FILE = r'C:\Users\lap4all\Desktop\Backlog_Automation\credentials.json'
if not os.path.exists(JSON_FILE):
    JSON_FILE = 'credentials.json'

SPREADSHEET_ID = '1XaziS_8UB2lCwL01bxam106EdIUHtlMISDGJX1PU5A8'

def main():
    print("Connecting to Google Sheets...")
    creds = Credentials.from_service_account_file(
        JSON_FILE, 
        scopes=['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
    )
    gc = gspread.authorize(creds)
    sh = gc.open_by_key(SPREADSHEET_ID)
    print(f"Connected to sheet: '{sh.title}'")

    print("Attempting to write to cell Z1 on 'tong_quan' sheet...")
    ws = sh.worksheet('tong_quan')
    try:
        ws.update(range_name='Z1', values=[['test_write']], value_input_option='USER_ENTERED')
        print("Successfully wrote to Z1 on 'tong_quan'!")
    except Exception as e:
        print(f"Failed to write to Z1 on 'tong_quan': {e}")

    print("\nAttempting to create a new temporary worksheet...")
    try:
        temp_ws = sh.add_worksheet(title="temp_test_write", rows="10", cols="10")
        print("Successfully created 'temp_test_write' worksheet!")
        print("Deleting temporary worksheet...")
        sh.del_worksheet(temp_ws)
        print("Successfully deleted temporary worksheet!")
    except Exception as e:
        print(f"Failed to create/delete worksheet: {e}")

if __name__ == '__main__':
    main()
