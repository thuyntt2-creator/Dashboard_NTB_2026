import sys
import pandas as pd
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

sys.stdout.reconfigure(encoding='utf-8')

SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
sheet_id = '1PjzFqJO-wkQ8SNsPHD721_CbPr6c_ArZKuGGU6KqDZg'

creds = Credentials.from_authorized_user_file('authorized_user.json', SCOPES)
service = build('sheets', 'v4', credentials=creds)

TAB_NAME = 'Tổng Hợp KA OFF'

# 1. Read the clean CSV
df = pd.read_csv("scratch/tong_hop_ka_off.csv", dtype=str)
# Fix row 10 (Nghĩa Tân)
df.loc[df['Phường/xã cần tắt'] == 'Phường Nghĩa Tân', 'Bưu Cục'] = '(DNO) Đông Gia Nghĩa'
df.loc[df['Phường/xã cần tắt'] == 'Phường Nghĩa Tân', 'AM'] = 'Huỳnh Thúc Duân'

# 2. Check if tab exists
meta = service.spreadsheets().get(spreadsheetId=sheet_id).execute()
existing_sheets = {s['properties']['title']: s['properties']['sheetId'] for s in meta.get('sheets', [])}

if TAB_NAME not in existing_sheets:
    print(f"Creating tab '{TAB_NAME}'...")
    body = {
        'requests': [{
            'addSheet': {
                'properties': {
                    'title': TAB_NAME,
                    'tabColor': {'red': 0.2, 'green': 0.6, 'blue': 0.86}
                }
            }
        }]
    }
    res = service.spreadsheets().batchUpdate(spreadsheetId=sheet_id, body=body).execute()
    new_sheet_id = res['replies'][0]['addSheet']['properties']['sheetId']
    print(f"Created tab '{TAB_NAME}' with sheetId {new_sheet_id}")
else:
    new_sheet_id = existing_sheets[TAB_NAME]
    print(f"Tab '{TAB_NAME}' already exists (sheetId {new_sheet_id}). Clearing content...")
    service.spreadsheets().values().clear(spreadsheetId=sheet_id, range=f"'{TAB_NAME}'!A1:Z100").execute()

# 3. Write data
headers = list(df.columns)
values = [headers] + df.values.tolist()

body = {
    'values': values
}
service.spreadsheets().values().update(
    spreadsheetId=sheet_id,
    range=f"'{TAB_NAME}'!A1",
    valueInputOption='USER_ENTERED',
    body=body
).execute()
print(f"Updated {len(values)} rows in tab '{TAB_NAME}'!")

# 4. Format header (bold, background color)
requests = [
    {
        'repeatCell': {
            'range': {
                'sheetId': new_sheet_id,
                'startRowIndex': 0,
                'endRowIndex': 1,
                'startColumnIndex': 0,
                'endColumnIndex': len(headers)
            },
            'cell': {
                'userEnteredFormat': {
                    'backgroundColor': {'red': 0.15, 'green': 0.35, 'blue': 0.6},
                    'textFormat': {'foregroundColor': {'red': 1.0, 'green': 1.0, 'blue': 1.0}, 'bold': True, 'fontSize': 10},
                    'horizontalAlignment': 'CENTER'
                }
            },
            'fields': 'userEnteredFormat(backgroundColor,textFormat,horizontalAlignment)'
        }
    },
    {
        'autoResizeDimensions': {
            'dimensions': {
                'sheetId': new_sheet_id,
                'dimension': 'COLUMNS',
                'startIndex': 0,
                'endIndex': len(headers)
            }
        }
    }
]

service.spreadsheets().batchUpdate(spreadsheetId=sheet_id, body={'requests': requests}).execute()
print("Formatting applied successfully!")
