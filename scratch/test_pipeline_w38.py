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
df_tq['am'] = df_tq['AM_format'].str.strip()

ws_f30 = doc.worksheet('f30')
df_f30 = pd.DataFrame(ws_f30.get_all_values()[1:], columns=ws_f30.get_all_values()[0])
df_f30['d'] = pd.to_datetime(df_f30['NgayDate'], format='%d/%m/%Y', errors='coerce')
df_f30['dt'] = pd.to_numeric(df_f30['DoanhThu_NoVAT'], errors='coerce').fillna(0)
df_f30['vol'] = pd.to_numeric(df_f30['Volume'], errors='coerce').fillna(0)
df_f30['am'] = df_f30['AM'].str.strip()

def process_pipeline(tq_curr_range, tq_prev_range, f30_curr_range, f30_prev_range):
    # KD
    sub_c = df_tq[(df_tq['d'] >= tq_curr_range[0]) & (df_tq['d'] <= tq_curr_range[1])]
    sub_p = df_tq[(df_tq['d'] >= tq_prev_range[0]) & (df_tq['d'] <= tq_prev_range[1])]
    
    am_c = sub_c.groupby('am').agg({'dt': 'sum', 'vol': 'sum'})
    am_p = sub_p.groupby('am').agg({'dt': 'sum', 'vol': 'sum'})
    
    all_ams = sorted(list(set(am_c.index) | set(am_p.index)))
    total_rev_c = sub_c['dt'].sum()
    total_rev_p = sub_p['dt'].sum()
    total_vol_c = sub_c['vol'].sum()
    total_vol_p = sub_p['vol'].sum()
    
    kd_am = []
    for a in all_ams:
        rc = float(am_c.loc[a, 'dt']) if a in am_c.index else 0.0
        rp = float(am_p.loc[a, 'dt']) if a in am_p.index else 0.0
        vc = int(am_c.loc[a, 'vol']) if a in am_c.index else 0
        vp = int(am_p.loc[a, 'vol']) if a in am_p.index else 0
        diff_r = rc - rp
        pct_diff_r = round((diff_r / rp) * 100, 1) if rp > 0 else (100.0 if rc > 0 else 0.0)
        pct_r = round((rc / total_rev_c) * 100, 1) if total_rev_c > 0 else 0.0
        kd_am.append({
            'am': a,
            'vol_prev': vp,
            'vol_curr': vc,
            'diff_vol': vc - vp,
            'rev_prev': rc,
            'rev_curr': rc,
            'diff_rev': diff_r,
            'pct_rev': pct_r,
            'pct_diff_rev': pct_diff_r
        })
    kd_am.sort(key=lambda x: x['rev_curr'], reverse=True)
    
    # F30
    f_c = df_f30[(df_f30['d'] >= f30_curr_range[0]) & (df_f30['d'] <= f30_curr_range[1])]
    f_p = df_f30[(df_f30['d'] >= f30_prev_range[0]) & (df_f30['d'] <= f30_prev_range[1])]
    
    f_am_c = f_c.groupby('am').agg({'dt': 'sum', 'Mã KH': 'count'})
    f_am_p = f_p.groupby('am').agg({'dt': 'sum', 'Mã KH': 'count'})
    
    all_f_ams = sorted(list(set(f_am_c.index) | set(f_am_p.index)))
    f30_am = []
    for a in all_f_ams:
        kc = int(f_am_c.loc[a, 'Mã KH']) if a in f_am_c.index else 0
        kp = int(f_am_p.loc[a, 'Mã KH']) if a in f_am_p.index else 0
        rc = float(f_am_c.loc[a, 'dt']) if a in f_am_c.index else 0.0
        rp = float(f_am_p.loc[a, 'dt']) if a in f_am_p.index else 0.0
        diff_k = kc - kp
        diff_r = rc - rp
        pct_k = round((diff_k / kp) * 100, 1) if kp > 0 else (100.0 if kc > 0 else 0.0)
        f30_am.append({
            'am': a,
            'kh_prev': kp,
            'kh_curr': kc,
            'diff_kh': diff_k,
            'pct_diff_kh': pct_k,
            'rev_prev': rp,
            'rev_curr': rc,
            'diff_rev': diff_r
        })
    f30_am.sort(key=lambda x: x['kh_curr'], reverse=True)
    
    return {
        'total_rev_curr': total_rev_c,
        'total_rev_prev': total_rev_p,
        'diff_rev': total_rev_c - total_rev_p,
        'pct_diff_rev': round((total_rev_c - total_rev_p) / total_rev_p * 100, 1) if total_rev_p > 0 else 0,
        'total_vol_curr': total_vol_c,
        'total_vol_prev': total_vol_p,
        'diff_vol': total_vol_c - total_vol_p,
        'total_f30_kh_curr': len(f_c),
        'total_f30_kh_prev': len(f_p),
        'diff_f30_kh': len(f_c) - len(f_p),
        'total_f30_rev_curr': f_c['dt'].sum(),
        'total_f30_rev_prev': f_p['dt'].sum(),
        'diff_f30_rev': f_c['dt'].sum() - f_p['dt'].sum(),
        'kd_am': kd_am,
        'f30_am': f30_am
    }

print("=== RUNNING FOR T38 (14/09-20/09) vs T37 (07/09-13/09) ===")
res38 = process_pipeline(('2026-09-14', '2026-09-20'), ('2026-09-07', '2026-09-13'), ('2026-09-14', '2026-09-20'), ('2026-09-07', '2026-09-13'))
print(f"Doanh thu: {res38['total_rev_curr']:,.0f} đ vs {res38['total_rev_prev']:,.0f} đ (diff: {res38['diff_rev']:,.0f} đ, {res38['pct_diff_rev']}%)")
print(f"Volume: {res38['total_vol_curr']:,} vs {res38['total_vol_prev']:,} (diff: {res38['diff_vol']:,})")
print(f"F30 KH: {res38['total_f30_kh_curr']} vs {res38['total_f30_kh_prev']} (diff: {res38['diff_f30_kh']})")
print(f"F30 DT: {res38['total_f30_rev_curr']:,.0f} đ vs {res38['total_f30_rev_prev']:,.0f} đ (diff: {res38['diff_f30_rev']:,.0f} đ)")
print("Top 3 AM Doanh Thu:", [(x['am'], f"{x['rev_curr']:,.0f}", f"{x['pct_rev']}%") for x in res38['kd_am'][:3]])
print("Top 3 AM F30:", [(x['am'], x['kh_curr'], f"{x['rev_curr']:,.0f}") for x in res38['f30_am'][:3]])
