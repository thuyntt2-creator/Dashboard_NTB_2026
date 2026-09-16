import sys
import pandas as pd
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

sys.stdout.reconfigure(encoding='utf-8')
creds = Credentials.from_authorized_user_file('authorized_user.json')
service = build('sheets', 'v4', credentials=creds)
ss_id = '1JZ1eRerRqrpwjZ4HBevQunjd8VquM_cvPFz12TaJfMQ'

res = service.spreadsheets().values().get(spreadsheetId=ss_id, range="'Đang off'!A1:Z200").execute()
values = res.get('values', [])
print(f"Total online rows: {len(values)}")
headers = values[0]
print("Online Headers:", headers)

online_df = pd.DataFrame(values[1:], columns=headers)
print("\nOnline Data Summary:")
print(online_df.to_string())

# Also check local off_tuyen_spe.csv
local_df = pd.read_csv('off_tuyen_spe.csv', encoding='utf-8')
print(f"\nLocal CSV rows: {len(local_df)}")
print("Local CSV Headers:", list(local_df.columns))

# Compare differences
print("\n--- DIFFERENCE CHECK ---")
print("Online count:", len(online_df), "vs Local count:", len(local_df))

# Let's inspect each row
diffs = []
for i in range(max(len(online_df), len(local_df))):
    on_row = online_df.iloc[i].to_dict() if i < len(online_df) else None
    loc_row = local_df.iloc[i].to_dict() if i < len(local_df) else None
    if on_row != loc_row:
        diffs.append((i, on_row, loc_row))

print(f"Total different rows: {len(diffs)}")
for i, on_r, loc_r in diffs:
    print(f"\nRow {i+1}:")
    print(f"  Online: {on_r}")
    print(f"  Local : {loc_r}")
