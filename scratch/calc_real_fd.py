import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import pandas as pd

creds = Credentials.from_authorized_user_file('authorized_user.json', ['https://www.googleapis.com/auth/spreadsheets'])
service = build('sheets', 'v4', credentials=creds)

source_sheet_id = "1odUPX5mWpUYUUQOrhX_k8kXWV7drMUdQ58DRwgSQNS8"
target_sheet_id = "15Z-aMM6OFfiWUXd2Zwz6BFNq_Y0KWwHiVDqxkioHufM"

# Read CoCauVung from target sheet
res_cocau = service.spreadsheets().values().get(
    spreadsheetId=target_sheet_id,
    range="'CoCauVung'!A1:D200"
).execute()
cocau_rows = res_cocau.get('values', [])
bc_to_am = {}
if len(cocau_rows) > 1:
    for r in cocau_rows[1:]:
        if len(r) >= 4:
            bc_to_am[r[1].strip()] = r[3].strip()

# Read Master FD rows (last 20,000 rows where 9/3/2026 would be)
res_data = service.spreadsheets().values().get(
    spreadsheetId=source_sheet_id,
    range="'FD'!A35000:G55200"
).execute()

rows = res_data.get('values', [])
print(f"Fetched {len(rows)} rows from Master FD")

ntb_n1_rows = []
for r in rows:
    if len(r) >= 7:
        date_val = r[0].strip()
        region_val = r[1].strip()
        if region_val == 'NTB' and (date_val == '9/3/2026' or '9/3' in date_val):
            ntb_n1_rows.append(r[:7])

print(f"Total NTB N-1 rows found: {len(ntb_n1_rows)}")
if ntb_n1_rows:
    df = pd.DataFrame(ntb_n1_rows, columns=['date', 'region', 'id', 'bc', 'client_type', 'total', 'return'])
    df['total'] = pd.to_numeric(df['total'].astype(str).str.replace(',', ''), errors='coerce').fillna(0)
    df['return'] = pd.to_numeric(df['return'].astype(str).str.replace(',', ''), errors='coerce').fillna(0)
    
    # Filter out kho giao hang
    df = df[~df['bc'].str.lower().str.contains('kho giao hàng', na=False)]
    
    df['am'] = df['bc'].map(bc_to_am)
    df_valid = df[df['am'].notna() & (df['am'] != '')]
    
    print(f"Valid rows with AM: {len(df_valid)}")
    tot_don = df_valid['total'].sum()
    tot_ret = df_valid['return'].sum()
    pct_fd = (tot_ret / tot_don * 100) if tot_don > 0 else 0
    print(f"\n--- REAL NTB N-1 SUMMARY ---")
    print(f"Total đơn gán giao: {tot_don:,.0f}")
    print(f"Total đơn return:   {tot_ret:,.0f}")
    print(f"%FD NTB:            {pct_fd:.2f}%")
    
    # Check Đức Lập
    dl = df_valid[df_valid['bc'] == '(DNO) Đức Lập']
    print("\nĐức Lập:")
    print(dl[['client_type', 'total', 'return']])
    print(f"Đức Lập Total: {dl['total'].sum()}, Return: {dl['return'].sum()}, %FD: {dl['return'].sum()/dl['total'].sum()*100:.2f}%")
    
    # Top 10 by %FD
    bc_agg = df_valid.groupby(['id', 'bc', 'am']).agg({'total': 'sum', 'return': 'sum'}).reset_index()
    bc_agg['%FD'] = (bc_agg['return'] / bc_agg['total'] * 100).round(2)
    bc_agg['ty_trong_ret'] = (bc_agg['return'] / tot_ret * 100).round(2)
    top10 = bc_agg.sort_values('%FD', ascending=False).head(10)
    print("\n--- TOP 10 BƯU CỤC %FD CAO NHẤT ---")
    print(top10[['bc', 'am', 'total', 'return', '%FD', 'ty_trong_ret']])
