import gspread
import pandas as pd
import json

gc = gspread.oauth(authorized_user_filename='authorized_user.json')
doc = gc.open_by_key('1E9BdaxouCeTUBeGLh0kyieyWE6wZoymglbZw19LRKEo')

ws_tq = doc.worksheet('tong_quan')
df_tq = pd.DataFrame(ws_tq.get_all_values()[1:], columns=ws_tq.get_all_values()[0])
df_tq['d'] = pd.to_datetime(df_tq['NgayDate'], format='%d/%m/%Y', errors='coerce')
df_tq['dt'] = pd.to_numeric(df_tq['DoanhThu'], errors='coerce').fillna(0)
df_tq['vol'] = pd.to_numeric(df_tq['Volume'], errors='coerce').fillna(0)

ws_f30 = doc.worksheet('f30')
df_f30 = pd.DataFrame(ws_f30.get_all_values()[1:], columns=ws_f30.get_all_values()[0])
df_f30['d'] = pd.to_datetime(df_f30['NgayDate'], format='%d/%m/%Y', errors='coerce')
df_f30['dt'] = pd.to_numeric(df_f30['DoanhThu_NoVAT'], errors='coerce').fillna(0)
df_f30['vol'] = pd.to_numeric(df_f30['Volume'], errors='coerce').fillna(0)

def calc_periods(df, val_col, p_curr, p_prev, group_col='AM_format'):
    sub_curr = df[(df['d'] >= p_curr[0]) & (df['d'] <= p_curr[1])]
    sub_prev = df[(df['d'] >= p_prev[0]) & (df['d'] <= p_prev[1])]
    
    g_curr = sub_curr.groupby(group_col)[val_col].sum()
    g_prev = sub_prev.groupby(group_col)[val_col].sum()
    
    all_keys = sorted(list(set(g_curr.index) | set(g_prev.index)))
    res = []
    for k in all_keys:
        v_c = g_curr.get(k, 0)
        v_p = g_prev.get(k, 0)
        res.append({'key': k, 'curr': v_c, 'prev': v_p, 'diff': v_c - v_p})
    return res, sub_curr[val_col].sum(), sub_prev[val_col].sum()

print("=== OPTION 1: W37 (06/09-12/09) vs W36 (30/08-05/09) [Exact Tong quan T37] ===")
res_am, tot_c, tot_p = calc_periods(df_tq, 'dt', ('2026-09-06', '2026-09-12'), ('2026-08-30', '2026-09-05'))
print(f"Total DT: {tot_c:,.0f} vs {tot_p:,.0f} (diff: {tot_c-tot_p:,.0f}, {(tot_c-tot_p)/tot_p*100:.1f}%)")

print("\n=== OPTION 2: W38 (13/09-19/09) vs W37 (06/09-12/09) [Sun-Sat] ===")
res_am2, tot_c2, tot_p2 = calc_periods(df_tq, 'dt', ('2026-09-13', '2026-09-19'), ('2026-09-06', '2026-09-12'))
print(f"Total DT: {tot_c2:,.0f} vs {tot_p2:,.0f} (diff: {tot_c2-tot_p2:,.0f}, {(tot_c2-tot_p2)/tot_p2*100:.1f}%)")

print("\n=== OPTION 3: W38 (14/09-20/09) vs W37 (07/09-13/09) [Mon-Sun - GHN Standard] ===")
res_am3, tot_c3, tot_p3 = calc_periods(df_tq, 'dt', ('2026-09-14', '2026-09-20'), ('2026-09-07', '2026-09-13'))
print(f"Total DT: {tot_c3:,.0f} vs {tot_p3:,.0f} (diff: {tot_c3-tot_p3:,.0f}, {(tot_c3-tot_p3)/tot_p3*100:.1f}%)")

# F30 checks
def calc_f30(p_curr, p_prev):
    sub_curr = df_f30[(df_f30['d'] >= p_curr[0]) & (df_f30['d'] <= p_curr[1])]
    sub_prev = df_f30[(df_f30['d'] >= p_prev[0]) & (df_f30['d'] <= p_prev[1])]
    return len(sub_curr), sub_curr['dt'].sum(), len(sub_prev), sub_prev['dt'].sum()

print("\nF30 Option 1 (T37 vs T36):", calc_f30(('2026-09-06', '2026-09-12'), ('2026-08-30', '2026-09-05')))
print("F30 Option 2 (T38 vs T37 Sun-Sat):", calc_f30(('2026-09-13', '2026-09-19'), ('2026-09-06', '2026-09-12')))
print("F30 Option 3 (T38 vs T37 Mon-Sun):", calc_f30(('2026-09-14', '2026-09-20'), ('2026-09-07', '2026-09-13')))
