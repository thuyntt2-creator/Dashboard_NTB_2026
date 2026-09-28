import pandas as pd, sys
sys.stdout.reconfigure(encoding='utf-8')

df = pd.read_csv('ops_gtc.csv')
w39_dates = [
    '2026-09-21 - Thứ 2', '2026-09-22 - Thứ 3', '2026-09-23 - Thứ 4',
    '2026-09-24 - Thứ 5', '2026-09-25 - Thứ 6', '2026-09-26 - Thứ 7',
    '2026-09-27 - Chủ Nhật'
]

matches = df[(df['Chi tiết'].astype(str).str.contains('Lâm Viên.*2', regex=True, na=False)) & (df['Time'].isin(w39_dates))].copy()

cols = ['Time', 'Loại Hàng', 'Volume', '% Gán', '% GTC', 'Sản Lượng Giao Thành Công', 'Sản Lượng Tồn']
print(matches.sort_values(by=['Loại Hàng', 'Time'])[cols].to_string())

print('\n=== TỔNG HỢP THEO LOẠI HÀNG TUẦN W39 CỦA BƯU CỤC LÂM VIÊN 2 ===')
for loai, grp in matches.groupby('Loại Hàng'):
    vol = grp['Volume'].astype(str).str.replace(',', '').astype(float).sum()
    gtc_vol = grp['Sản Lượng Giao Thành Công'].astype(str).str.replace(',', '').astype(float).sum()
    ton_vol = grp['Sản Lượng Tồn'].astype(str).str.replace(',', '').astype(float).sum()
    pct_gtc = (gtc_vol / vol) * 100 if vol > 0 else 0
    print(f"{loai}: Volume = {vol:,.0f} | GTC = {gtc_vol:,.0f} đơn ({pct_gtc:.2f}%) | Tồn = {ton_vol:,.0f} đơn")

# Overall total
tot_vol = matches['Volume'].astype(str).str.replace(',', '').astype(float).sum()
tot_gtc = matches['Sản Lượng Giao Thành Công'].astype(str).str.replace(',', '').astype(float).sum()
tot_ton = matches['Sản Lượng Tồn'].astype(str).str.replace(',', '').astype(float).sum()
print(f"\n==> TỔNG CỘNG LÂM VIÊN 2 (W39): Volume = {tot_vol:,.0f} | GTC = {tot_gtc:,.0f} đơn ({tot_gtc/tot_vol*100:.2f}%) | Tồn = {tot_ton:,.0f} đơn")
