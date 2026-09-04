import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import json

creds = Credentials.from_authorized_user_file('authorized_user.json', ['https://www.googleapis.com/auth/spreadsheets'])
service = build('sheets', 'v4', credentials=creds)
target_sheet_id = "15Z-aMM6OFfiWUXd2Zwz6BFNq_Y0KWwHiVDqxkioHufM"

# 1. Update A1 formula in RAW FD N-1 (HUB) to include Column G (A1:G40000 etc.)
new_a1_formula = '''=QUERY(
  {
    IFERROR(IMPORTRANGE("1odUPX5mWpUYUUQOrhX_k8kXWV7drMUdQ58DRwgSQNS8", "FD!A1:G40000"), {"","","","","","",""});
    IFERROR(IMPORTRANGE("1odUPX5mWpUYUUQOrhX_k8kXWV7drMUdQ58DRwgSQNS8", "FD!A40001:G80000"), {"","","","","","",""});
    IFERROR(IMPORTRANGE("1odUPX5mWpUYUUQOrhX_k8kXWV7drMUdQ58DRwgSQNS8", "FD!A80001:G120000"), {"","","","","","",""});
    IFERROR(IMPORTRANGE("1odUPX5mWpUYUUQOrhX_k8kXWV7drMUdQ58DRwgSQNS8", "FD!A120001:G160000"), {"","","","","","",""})
  },
  "SELECT * WHERE Col2 = 'NTB' AND Col1 = " & INT(TODAY()-1) & " AND NOT lower(Col4) CONTAINS 'kho giao hàng'",
  1
)'''

# In Col G row 1 was 'AM', but now Col G will be 'Đơn return' from the query!
# So we must clear old G1 and G2, and put 'AM' in H1 and formula in H2!
body = {
    'valueInputOption': 'USER_ENTERED',
    'data': [
        {
            'range': "'RAW FD N-1 (HUB)'!A1",
            'values': [[new_a1_formula]]
        },
        {
            'range': "'RAW FD N-1 (HUB)'!G1:G2",
            'values': [[''], ['']] # clear old AM in G1:G2
        },
        {
            'range': "'RAW FD N-1 (HUB)'!H1:H2",
            'values': [
                ['AM'],
                ['=ARRAYFORMULA(IF(C2:C="", "", IFERROR(VLOOKUP(C2:C, CoCauVung!A:D, 4, FALSE), "")))']
            ]
        }
    ]
}

res = service.spreadsheets().values().batchUpdate(
    spreadsheetId=target_sheet_id,
    body=body
).execute()

print("Updated RAW FD N-1 (HUB) formulas successfully:", res)
