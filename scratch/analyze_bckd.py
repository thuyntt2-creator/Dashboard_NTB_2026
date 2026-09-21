import gspread, json, sys, pandas as pd
from datetime import datetime
sys.stdout.reconfigure(encoding='utf-8')
from google.oauth2.credentials import Credentials

with open('authorized_user.json', 'r', encoding='utf-8') as f:
    info = json.load(f)
creds = Credentials.from_authorized_user_info(info)
gc = gspread.authorize(creds)

sheet_id = '1E9BdaxouCeTUBeGLh0kyieyWE6wZoymglbZw19LRKEo'
sh = gc.open_by_key(sheet_id)

ws_tq = sh.worksheet('tong_quan')
data_tq = ws_tq.get_all_values()
df_tq = pd.DataFrame(data_tq[1:], columns=data_tq[0])
print('=== tong_quan === Shape:', df_tq.shape)

df_tq['date'] = pd.to_datetime(df_tq['NgayDate'], format='%d/%m/%Y', errors='coerce')
df_tq['DT'] = pd.to_numeric(df_tq['DoanhThu'], errors='coerce').fillna(0)
df_tq['Vol'] = pd.to_numeric(df_tq['Volume'], errors='coerce').fillna(0)

print('Min date in tong_quan:', df_tq['date'].min(), 'Max date:', df_tq['date'].max())

weeks = [
    ('2026-08-30', '2026-09-05', 'T36 (30/08-05/09)'),
    ('2026-09-06', '2026-09-12', 'T37 (06/09-12/09)'),
    ('2026-09-07', '2026-09-13', 'T37 alt (07/09-13/09)'),
    ('2026-09-13', '2026-09-19', 'T38 (13/09-19/09)'),
    ('2026-09-14', '2026-09-20', 'T38 (14/09-20/09)')
]

for start, end, name in weeks:
    sub = df_tq[(df_tq['date'] >= start) & (df_tq['date'] <= end)]
    dt_sum = sub['DT'].sum()
    vol_sum = sub['Vol'].sum()
    print(f"{name}: {len(sub)} rows | DoanhThu: {dt_sum:,.0f} đ | Volume: {vol_sum:,.0f}")

# Also analyze f30
ws_f30 = sh.worksheet('f30')
data_f30 = ws_f30.get_all_values()
df_f30 = pd.DataFrame(data_f30[1:], columns=data_f30[0])
print('\n=== f30 === Shape:', df_f30.shape)

df_f30['date'] = pd.to_datetime(df_f30['NgayDate'], format='%d/%m/%Y', errors='coerce')
df_f30['DT'] = pd.to_numeric(df_f30['DoanhThu_NoVAT'], errors='coerce').fillna(0)
df_f30['Vol'] = pd.to_numeric(df_f30['Volume'], errors='coerce').fillna(0)

print('Min date in f30:', df_f30['date'].min(), 'Max date:', df_f30['date'].max())

for start, end, name in weeks:
    sub = df_f30[(df_f30['date'] >= start) & (df_f30['date'] <= end)]
    dt_sum = sub['DT'].sum()
    vol_sum = sub['Vol'].sum()
    kh_count = sub['Mã KH'].nunique()
    print(f"{name}: {len(sub)} rows | KH: {kh_count} | DoanhThu: {dt_sum:,.0f} đ | Volume: {vol_sum:,.0f}")
