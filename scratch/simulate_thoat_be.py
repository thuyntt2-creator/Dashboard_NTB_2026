# -*- coding: utf-8 -*-
import sys, math
import pandas as pd
from datetime import datetime
from google.oauth2.credentials import Credentials
import gspread

sys.stdout.reconfigure(encoding='utf-8')

# 1. Đọc file thực tế của Chị Thủy
excel_path = r'C:\Users\lap4all\Downloads\Bao_cao_ton_dong_lay_giao_tra_2026-10-20_at_09_00_03.xlsx'
df = pd.read_excel(excel_path, header=1)
df_giao = df[df['Loại đơn'].isin(['Giao', 'Ưu tiên giao'])]
agg = df_giao.groupby('Mã bưu cục')['Mã đơn hàng'].count().to_dict()

# 2. Đọc Google Sheet
creds = Credentials.from_authorized_user_file('authorized_user.json', ['https://www.googleapis.com/auth/spreadsheets'])
gc = gspread.authorize(creds)
sh = gc.open_by_key('14cN4YAf01NqKtREtmhBngRP58OCdgby-PjVoixVlpZo')

# Đọc cấu hình bưu cục cảnh báo
ws_bo = sh.worksheet('Bất ổn')
rows_bo = ws_bo.get_values('C5:F25')
bc_dict = {}
for r in rows_bo:
    if len(r) >= 4 and r[0].strip():
        try:
            bc_id = int(r[0].strip())
            name = r[1].strip()
            best = float(r[3].replace('%', '').strip()) / 100.0
            bc_dict[name] = {'id': bc_id, 'best': best}
        except Exception as e:
            pass

# Đọc lịch sử 'Theo dõi BC bể'
ws_td = sh.worksheet('Theo dõi BC bể')
rows_td = ws_td.get_all_values()

def parse_d(s):
    try:
        if str(s).isdigit():
            return datetime.fromordinal(datetime(1899, 12, 30).toordinal() + int(s))
        for fmt in ['%d/%m/%Y', '%m/%d/%Y', '%Y-%m-%d']:
            try: return datetime.strptime(s, fmt)
            except: pass
    except: pass
    return datetime(1970, 1, 1)

history = {}
for r in rows_td[1:]:
    name = r[0].strip()
    if name in bc_dict:
        if name not in history: history[name] = []
        try:
            d = parse_d(r[1])
            cd = int(r[2].replace(',', '')) + int(r[3].replace(',', ''))
            gtc = int(r[6].replace(',', ''))
            history[name].append({'date': d, 'cd': cd, 'gtc': gtc})
        except: pass

print("="*80)
print("PHÂN TÍCH VÀ MÔ PHỎNG: NẾU GIAO ĐÚNG TARGET, CÓ THOÁT BỂ ĐƯỢC THẬT KHÔNG?")
print("="*80)

for name, info in bc_dict.items():
    bc_id = info['id']
    best = info['best']
    
    # 6 ngày gần nhất thực tế (Tháng 10: 14/10 -> 19/10)
    sorted_hist = sorted(history.get(name, []), key=lambda x: x['date'], reverse=True)[:6]
    s_vol_6 = sum([x['cd'] for x in sorted_hist])
    s_gtc_6 = sum([x['gtc'] for x in sorted_hist])
    
    # Volume thực tế hôm nay (từ file Chị Thủy gửi)
    # Thử cả ID số và các định dạng
    vol_today = agg.get(bc_id, 0)
    if vol_today == 0:
        # Thử tìm theo mã bưu cục ngắn hoặc string
        for k, v in agg.items():
            if str(k) in str(bc_id) or str(bc_id) in str(k):
                vol_today = v
                break
                
    total_vol_7 = s_vol_6 + vol_today
    
    # Tính Target theo công thức logic
    dk1 = math.ceil(0.45 * total_vol_7 - s_gtc_6)
    dk2 = math.ceil(0.70 * best * total_vol_7 - s_gtc_6)
    target = max(dk1, dk2, math.ceil(0.20 * vol_today), 0)
    
    # MÔ PHỎNG: Nếu bưu cục giao ĐÚNG con số target này:
    simulated_gtc_today = min(target, vol_today) # giả sử giao tối đa target (nếu target <= vol)
    simulated_total_gtc_7 = s_gtc_6 + simulated_gtc_today
    
    pct_gtc_7d_simulated = (simulated_total_gtc_7 / total_vol_7) if total_vol_7 > 0 else 0
    ratio_vs_best = pct_gtc_7d_simulated / best if best > 0 else 0
    
    pass_45 = pct_gtc_7d_simulated >= 0.45
    pass_70_best = ratio_vs_best >= 0.70
    is_escaped = pass_45 and pass_70_best
    
    print(f"\n📍 Bưu cục: {name} (ID: {bc_id})")
    print(f"   • Mốc lịch sử tốt nhất: {best*100:.2f}% | Mục tiêu 70% lịch sử: {best*0.7*100:.2f}%")
    print(f"   • Quá khứ 6 ngày: Vol = {s_vol_6:,} đơn | GTC = {s_gtc_6:,} đơn (%GTC 6d: {s_gtc_6/s_vol_6*100:.1f}%)")
    print(f"   • Hàng về hôm nay (file tải 9h): {vol_today:,} đơn")
    print(f"   • Target cần giao: {target:,} đơn")
    
    if target > vol_today:
        print(f"   ⚠️ KHÔNG THỂ THOÁT TRONG 1 NGÀY: Cần {target:,} đơn nhưng kho chỉ có {vol_today:,} đơn!")
        print(f"      (Dù giao sạch 100% hàng hôm nay thì %GTC 7 ngày mới đạt: {(s_gtc_6 + vol_today)/total_vol_7*100:.2f}%)")
        print(f"      => CẦN THÊM NGÀY để các ngày cũ trôi đi!")
    else:
        print(f"   ✅ NẾU HÔM NAY GIAO ĐƯỢC {target:,} / {vol_today:,} ĐƠN:")
        print(f"      - %GTC 7 ngày đạt: {pct_gtc_7d_simulated*100:.2f}% (Chuẩn >= 45%: {'ĐẠT' if pass_45 else 'HỤT'})")
        print(f"      - So với lịch sử tốt nhất: {ratio_vs_best*100:.1f}% (Chuẩn >= 70%: {'ĐẠT' if pass_70_best else 'HỤT'})")
        print(f"      => KẾT LUẬN: {'🎉 THẬT SỰ THOÁT BỂ 100%!' if is_escaped else '❌ VẪN BỊ DÍNH CẢNH BÁO'}")
