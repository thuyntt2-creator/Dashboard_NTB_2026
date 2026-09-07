import pandas as pd
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
csv_name = 'sheet_Danh_sách_KH_không_lên_đơn_sv_ngày_hôm_qua_hoặc_giảm_đơn_sv_cùng_kỳ_tuần_trước.csv'
df = pd.read_csv(csv_name).dropna(how='all')

def parse_date(d_str):
    if not isinstance(d_str, str): return None
    m = re.match(r'(\d+)\s+thg\s+(\d+),\s+(\d+)', d_str.strip())
    if m:
        day, month, year = m.groups()
        return pd.Timestamp(f'{year}-{int(month):02d}-{int(day):02d}')
    return pd.to_datetime(d_str, errors='coerce')

df['dt_date'] = df['Ngaynext'].apply(parse_date)

print("Dates available in sheet:", sorted(df['dt_date'].dt.strftime('%Y-%m-%d').unique()))

# Option 1: 23-29/8 (W35) vs 30/8-5/9 (W36) (Exactly matching Kinh Doanh sheet 10)
prev_df = df[(df['dt_date'] >= '2026-08-23') & (df['dt_date'] <= '2026-08-29')]
curr_df = df[(df['dt_date'] >= '2026-08-30') & (df['dt_date'] <= '2026-09-05')]

p_agg = prev_df.groupby(['MaKH', 'TenKH', 'AM', 'Bưu cục'])['DT'].sum().reset_index().rename(columns={'DT': 'vol_prev'})
c_agg = curr_df.groupby(['MaKH', 'TenKH', 'AM', 'Bưu cục'])['DT'].sum().reset_index().rename(columns={'DT': 'vol_curr'})

m = pd.merge(p_agg, c_agg, on=['MaKH', 'TenKH', 'AM', 'Bưu cục'], how='outer').fillna(0)
m['diff'] = m['vol_curr'] - m['vol_prev']
m['pct_diff'] = (m['diff'] / m['vol_prev']).replace([float('inf'), -float('inf')], 0) * 100

print("\n==================================================================================")
print("TOP 15 KH GIẢM VOL / RỜI BỎ NHIỀU NHẤT (Kỳ 23–29/8 vs Kỳ 30/8–5/9) [Chuẩn KD]")
print("==================================================================================")
top15 = m.sort_values(by='diff', ascending=True).head(15)
for i, (_, r) in enumerate(top15.iterrows(), 1):
    status = "🔴 RỜI BỎ (Về 0)" if r['vol_curr'] == 0 else f"🟡 GIẢM MẠNH ({r['pct_diff']:.1f}%)"
    print(f"{i:2d}. [{int(r['MaKH'])}] {r['TenKH']}")
    print(f"    AM: {r['AM']} | Bưu cục: {r['Bưu cục']}")
    print(f"    Vol kỳ trước (23–29/8): {r['vol_prev']:.0f} đơn  ➔  Kỳ này (30/8–5/9): {r['vol_curr']:.0f} đơn | Δ: {r['diff']:.0f} đơn ({status})")

# Option 2: 24-30/8 vs 31/8-6/9 (Full Monday to Sunday W36 vs W35)
prev_w = df[(df['dt_date'] >= '2026-08-24') & (df['dt_date'] <= '2026-08-30')]
curr_w = df[(df['dt_date'] >= '2026-08-31') & (df['dt_date'] <= '2026-09-06')]

p_agg_w = prev_w.groupby(['MaKH', 'TenKH', 'AM', 'Bưu cục'])['DT'].sum().reset_index().rename(columns={'DT': 'vol_prev'})
c_agg_w = curr_w.groupby(['MaKH', 'TenKH', 'AM', 'Bưu cục'])['DT'].sum().reset_index().rename(columns={'DT': 'vol_curr'})

m_w = pd.merge(p_agg_w, c_agg_w, on=['MaKH', 'TenKH', 'AM', 'Bưu cục'], how='outer').fillna(0)
m_w['diff'] = m_w['vol_curr'] - m_w['vol_prev']
m_w['pct_diff'] = (m_w['diff'] / m_w['vol_prev']).replace([float('inf'), -float('inf')], 0) * 100

print("\n==================================================================================")
print("TOP 15 KH GIẢM VOL / RỜI BỎ NHIỀU NHẤT (Tuần W35 24–30/8 vs Tuần W36 31/8–6/9)")
print("==================================================================================")
top15_w = m_w.sort_values(by='diff', ascending=True).head(15)
for i, (_, r) in enumerate(top15_w.iterrows(), 1):
    status = "🔴 RỜI BỎ (Về 0)" if r['vol_curr'] == 0 else f"🟡 GIẢM MẠNH ({r['pct_diff']:.1f}%)"
    print(f"{i:2d}. [{int(r['MaKH'])}] {r['TenKH']}")
    print(f"    AM: {r['AM']} | Bưu cục: {r['Bưu cục']}")
    print(f"    Vol W35: {r['vol_prev']:.0f} đơn  ➔  Vol W36: {r['vol_curr']:.0f} đơn | Δ: {r['diff']:.0f} đơn ({status})")
