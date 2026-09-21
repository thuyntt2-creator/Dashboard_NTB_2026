import gspread
import pandas as pd

gc = gspread.oauth(authorized_user_filename='authorized_user.json')
doc = gc.open_by_key('1E9BdaxouCeTUBeGLh0kyieyWE6wZoymglbZw19LRKEo')

ws_f30 = doc.worksheet('f30')
df_f30 = pd.DataFrame(ws_f30.get_all_values()[1:], columns=ws_f30.get_all_values()[0])
df_f30['d'] = pd.to_datetime(df_f30['NgayDate'], format='%d/%m/%Y', errors='coerce')
df_f30['dt'] = pd.to_numeric(df_f30['DoanhThu_NoVAT'], errors='coerce').fillna(0)
df_f30['vol'] = pd.to_numeric(df_f30['Volume'], errors='coerce').fillna(0)

print('=== f30 by week ===')
for label, (s, e) in [
    ('Tuần 36 (30/08 - 05/09)', ('2026-08-30', '2026-09-05')),
    ('Tuần 37 (06/09 - 12/09)', ('2026-09-06', '2026-09-12')),
    ('Tuần 37 alt (07/09 - 13/09)', ('2026-09-07', '2026-09-13')),
    ('Tuần 38 (13/09 - 19/09)', ('2026-09-13', '2026-09-19')),
    ('Tuần 38 (14/09 - 20/09)', ('2026-09-14', '2026-09-20')),
]:
    sub = df_f30[(df_f30['d'] >= s) & (df_f30['d'] <= e)]
    dt_sum = sub['dt'].sum()
    vol_sum = sub['vol'].sum()
    print(f'{label}: {len(sub)} KH | DoanhThu: {dt_sum:,.0f} đ | Volume: {vol_sum:,.0f}')

ws_tq = doc.worksheet('tong_quan')
vals_tq = ws_tq.get_all_values()
df_tq = pd.DataFrame(vals_tq[1:], columns=vals_tq[0])
df_tq['d'] = pd.to_datetime(df_tq['NgayDate'], format='%d/%m/%Y', errors='coerce')
df_tq['dt'] = pd.to_numeric(df_tq['DoanhThu'], errors='coerce').fillna(0)
df_tq['vol'] = pd.to_numeric(df_tq['Volume'], errors='coerce').fillna(0)

print('\n=== tong_quan by week ===')
for label, (s, e) in [
    ('Tuần 36 (30/08 - 05/09)', ('2026-08-30', '2026-09-05')),
    ('Tuần 37 (06/09 - 12/09)', ('2026-09-06', '2026-09-12')),
    ('Tuần 37 alt (07/09 - 13/09)', ('2026-09-07', '2026-09-13')),
    ('Tuần 38 (13/09 - 19/09)', ('2026-09-13', '2026-09-19')),
    ('Tuần 38 (14/09 - 20/09)', ('2026-09-14', '2026-09-20')),
]:
    sub = df_tq[(df_tq['d'] >= s) & (df_tq['d'] <= e)]
    dt_sum = sub['dt'].sum()
    vol_sum = sub['vol'].sum()
    print(f'{label}: {len(sub)} records | DoanhThu: {dt_sum:,.0f} đ | Volume: {vol_sum:,.0f}')
