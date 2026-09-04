import sys
import json
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

creds = Credentials.from_authorized_user_file('authorized_user.json', ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'])
service = build('sheets', 'v4', credentials=creds)

source_id = "15Z-aMM6OFfiWUXd2Zwz6BFNq_Y0KWwHiVDqxkioHufM"
out_data = {}
try:
    meta = service.spreadsheets().get(spreadsheetId=source_id).execute()
    out_data['title'] = meta.get('properties', {}).get('title')
    out_data['sheets'] = [s.get('properties') for s in meta.get('sheets', [])]
    
    res = service.spreadsheets().values().get(
        spreadsheetId=source_id,
        range="'Snapshot – FD N-1 (HUB)'!A1:G100"
    ).execute()
    out_data['values'] = res.get('values', [])

    res_f = service.spreadsheets().values().get(
        spreadsheetId=source_id,
        range="'Snapshot – FD N-1 (HUB)'!A1:G40",
        valueRenderOption='FORMULA'
    ).execute()
    out_data['formulas'] = res_f.get('values', [])

    with open('scratch/source_fd_dump.json', 'w', encoding='utf-8') as f:
        json.dump(out_data, f, ensure_ascii=False, indent=2)
    print("Dumped successfully to scratch/source_fd_dump.json")
except Exception as e:
    print(f"Error: {e}")
