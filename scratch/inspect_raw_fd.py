import sys
import json
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

creds = Credentials.from_authorized_user_file('authorized_user.json', ['https://www.googleapis.com/auth/spreadsheets'])
service = build('sheets', 'v4', credentials=creds)

source_id = "15Z-aMM6OFfiWUXd2Zwz6BFNq_Y0KWwHiVDqxkioHufM"

# 1. Inspect RAW FD N-1 (HUB)
res_raw = service.spreadsheets().values().get(
    spreadsheetId=source_id,
    range="'RAW FD N-1 (HUB)'!A1:Z10"
).execute()

# 2. Inspect Snapshot – FD Tổng
res_tong = service.spreadsheets().values().get(
    spreadsheetId=source_id,
    range="'Snapshot – FD Tổng'!A1:M15"
).execute()

# 3. Check sheet "fd" in 1v_9VIJqyy0L3i8dqAUAOPjkhxcfi2HVc9IEGHiVNaDQ
try:
    res_ext = service.spreadsheets().values().get(
        spreadsheetId='1v_9VIJqyy0L3i8dqAUAOPjkhxcfi2HVc9IEGHiVNaDQ',
        range="fd!A1:V10"
    ).execute()
    ext_rows = res_ext.get('values', [])
except Exception as e:
    ext_rows = str(e)

out = {
    'raw_hub_header': res_raw.get('values', []),
    'snapshot_tong': res_tong.get('values', []),
    'ext_sheet': ext_rows
}

with open('scratch/inspect_raw_fd.json', 'w', encoding='utf-8') as f:
    json.dump(out, f, ensure_ascii=False, indent=2)

print("Saved to scratch/inspect_raw_fd.json")
