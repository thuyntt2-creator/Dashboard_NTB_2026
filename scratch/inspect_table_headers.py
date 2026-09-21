import sys
sys.stdout.reconfigure(encoding='utf-8')
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

creds = Credentials.from_authorized_user_file('authorized_user.json', ['https://www.googleapis.com/auth/spreadsheets'])
service = build('sheets', 'v4', credentials=creds)
work_id = '15Z-aMM6OFfiWUXd2Zwz6BFNq_Y0KWwHiVDqxkioHufM'

sheet_res = service.spreadsheets().get(
    spreadsheetId=work_id,
    ranges=["'Top 10 FD (T2-Gio)'!A9:D11", "'Top 10 FD (T2-Gio)'!A32:D34", "'Top 10 FD (T2-Gio)'!A39:D41", "'Top 10 FD (T2-Gio)'!A52:D54"],
    includeGridData=True
).execute()

for sheet in sheet_res['sheets']:
    for d in sheet['data']:
        for r_idx, r in enumerate(d.get('rowData', [])):
            for c_idx, c in enumerate(r.get('values', [])):
                val = c.get('formattedValue', '')
                fmt = c.get('userEnteredFormat', {})
                if val:
                    print(f"'{val}': bg={fmt.get('backgroundColor')}, fg={fmt.get('textFormat', {}).get('foregroundColor')}, bold={fmt.get('textFormat', {}).get('bold')}")
