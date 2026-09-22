import sys, json
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

sys.stdout.reconfigure(encoding='utf-8')
SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
creds = Credentials.from_authorized_user_file('authorized_user.json', SCOPES)
service = build('sheets', 'v4', credentials=creds)

sheet_ids = {
    'Link 1 (COD/QR)': '1j6Xm7JRemUGRSfbL-wc8DMwt7qfR7j79w9q79_snVnU',
    'Link 2 (Source)': '1hdJ_QhdiY4dhkW2JXBd5eHGH6r5ULqNao69nBDYWsoY',
    'Link 3 (Lap day/KTC)': '1rfoi8QaZSZNiYf8IyKNN4QLrjAVxCCGrX9Yli0D8T84'
}

for label, sid in sheet_ids.items():
    try:
        meta = service.spreadsheets().get(spreadsheetId=sid).execute()
        title = meta.get('properties', {}).get('title', '')
        sheets = [f"{s['properties']['title']} (gid={s['properties']['sheetId']})" for s in meta.get('sheets', [])]
        print(f"=== {label} | ID: {sid} ===")
        print(f"Title: {title}")
        print("Sheets:")
        for s in sheets:
            print("  -", s)
        print()
    except Exception as e:
        print(f"Error inspecting {label}: {e}")
