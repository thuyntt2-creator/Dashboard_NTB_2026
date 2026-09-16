import sys
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

sys.stdout.reconfigure(encoding='utf-8')
creds = Credentials.from_authorized_user_file('authorized_user.json')
service = build('sheets', 'v4', credentials=creds)
ss_id = '1JZ1eRerRqrpwjZ4HBevQunjd8VquM_cvPFz12TaJfMQ'

res = service.spreadsheets().get(
    spreadsheetId=ss_id,
    ranges=["'Đang off'!A1:Z50"],
    fields="sheets(data(rowData(values(formattedValue,userEnteredValue))))"
).execute()

sheet_data = res['sheets'][0]['data'][0]['rowData']
for r_idx, row in enumerate(sheet_data[:10]):
    row_vals = []
    for c_idx, cell in enumerate(row.get('values', [])):
        uev = cell.get('userEnteredValue', {})
        fv = cell.get('formattedValue', '')
        if 'formulaValue' in uev:
            row_vals.append(f"FORMULA({uev['formulaValue']})")
        else:
            row_vals.append(fv)
    print(f"Row {r_idx}: {row_vals[:9]}")
