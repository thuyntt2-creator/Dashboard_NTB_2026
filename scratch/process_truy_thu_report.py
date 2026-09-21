import pandas as pd
import numpy as np
import sys
import re
from datetime import datetime
import json
import os

sys.stdout.reconfigure(encoding='utf-8')

print("🚀 Running process_truy_thu_report.py (W37 vs W38 2-Week Comparison)...")

raw_path = 'sheet_truythu.csv'
if not os.path.exists(raw_path):
    raw_path = 'scratch/truythu_raw.csv'

if not os.path.exists(raw_path):
    print("❌ No truythu raw file found!")
    sys.exit(0)

tt = pd.read_csv(raw_path, low_memory=False)
print(f"Loaded {len(tt):,} rows from {raw_path}")

def parse_ghn_date(val):
    if not val or not isinstance(val, str):
        return None
    val = val.strip()
    m = re.search(r'(\d{1,2})\s+thg\s+(\d{1,2}),?\s+(\d{4})', val)
    if m:
        d, mth, y = int(m.group(1)), int(m.group(2)), int(m.group(3))
        return datetime(y, mth, d)
    m2 = re.search(r'(\d{4})-(\d{2})-(\d{2})', val)
    if m2:
        return datetime(int(m2.group(1)), int(m2.group(2)), int(m2.group(3)))
    m3 = re.search(r'(\d{1,2})/(\d{1,2})/(\d{4})', val)
    if m3:
        return datetime(int(m3.group(3)), int(m3.group(2)), int(m3.group(1)))
    return None

def parse_vn(s):
    try:
        return float(str(s).replace('.', '').replace(',', '.'))
    except:
        return 0.0

tt['date'] = tt['Ngày kết luận truy thu'].apply(parse_ghn_date)
tt['ban_dau'] = tt['Số tiền ban đầu'].apply(parse_vn)
tt['dieu_chinh'] = tt['Điều chỉnh (+|-)'].apply(parse_vn)
tt['da_thu'] = tt['Đã truy thu'].apply(parse_vn)
tt['can_thu'] = tt['Cần truy thu thêm'].apply(parse_vn)

# Filter 2 weeks
w_prev = tt[(tt['date'] >= datetime(2026, 9, 7)) & (tt['date'] <= datetime(2026, 9, 13))].copy()
w_curr = tt[(tt['date'] >= datetime(2026, 9, 14)) & (tt['date'] <= datetime(2026, 9, 20))].copy()

# AM and Province Mapping
am_rows = tt[tt['Chức vụ'].astype(str).str.contains('Area Manager', na=False)].copy()
am_rows['ten_am'] = am_rows['Nhân viên'].astype(str).apply(lambda x: x.split('-', 1)[1].strip() if '-' in x else x)
bc_am_map = {}
for bc, group in am_rows.groupby('Nơi vi phạm'):
    top_am = group['ten_am'].value_counts().index[0]
    bc_am_map[bc] = top_am

bc_tinh_map = {}
if os.path.exists('co_cau_ntb.csv'):
    cc = pd.read_csv('co_cau_ntb.csv')
    cols = cc.columns.tolist()
    name_col = next((c for c in cols if 'bưu cục' in c.lower() or 'warehouse' in c.lower() or 'tên' in c.lower()), cols[1])
    prov_col = next((c for c in cols if 'tỉnh' in c.lower() or 'province' in c.lower()), cols[2])
    am_col = next((c for c in cols if 'am' in c.lower()), None)
    for _, row in cc.iterrows():
        bc_name = str(row[name_col]).strip()
        prov_name = str(row[prov_col]).strip()
        bc_tinh_map[bc_name] = prov_name
        if am_col and bc_name not in bc_am_map:
            bc_am_map[bc_name] = str(row[am_col]).strip()

def get_province(bc):
    if bc in bc_tinh_map and bc_tinh_map[bc] and bc_tinh_map[bc] != 'nan':
        return bc_tinh_map[bc]
    if '(KHO)' in bc: return 'Khánh Hòa'
    if '(LDO)' in bc: return 'Lâm Đồng'
    if '(DNO)' in bc: return 'Đắk Nông'
    if '(BTH)' in bc: return 'Bình Thuận'
    if '(NTH)' in bc: return 'Ninh Thuận'
    return 'Khác'

w_prev['AM'] = w_prev['Nơi vi phạm'].map(bc_am_map).fillna('Chưa gán')
w_curr['AM'] = w_curr['Nơi vi phạm'].map(bc_am_map).fillna('Chưa gán')
w_prev['Tỉnh'] = w_prev['Nơi vi phạm'].apply(get_province)
w_curr['Tỉnh'] = w_curr['Nơi vi phạm'].apply(get_province)

# 1. Summary
rec_p = len(w_prev)
rec_c = len(w_curr)
diff_rec = rec_c - rec_p
diff_rec_pct = round(diff_rec / rec_p * 100, 1) if rec_p else 0

bd_p = float(w_prev['ban_dau'].sum())
bd_c = float(w_curr['ban_dau'].sum())
diff_bd = bd_c - bd_p
diff_bd_pct = round(diff_bd / bd_p * 100, 1) if bd_p else 0

dc_p = float(w_prev['dieu_chinh'].sum())
dc_c = float(w_curr['dieu_chinh'].sum())
diff_dc = dc_c - dc_p

ct_p = float(w_prev['can_thu'].sum())
ct_c = float(w_curr['can_thu'].sum())
diff_ct = ct_c - ct_p
diff_ct_pct = round(diff_ct / ct_p * 100, 1) if ct_p else 0

summary = {
    "prev_label": "Tuần W37 (07/09 - 13/09)",
    "curr_label": "Tuần W38 (14/09 - 20/09)",
    "total_records_prev": rec_p,
    "total_records_curr": rec_c,
    "diff_records": diff_rec,
    "diff_records_pct": f"{diff_rec_pct:+0.1f}%",
    "ban_dau_prev": bd_p,
    "ban_dau_curr": bd_c,
    "diff_ban_dau": diff_bd,
    "diff_ban_dau_pct": f"{diff_bd_pct:+0.1f}%",
    "dieu_chinh_prev": dc_p,
    "dieu_chinh_curr": dc_c,
    "diff_dieu_chinh": diff_dc,
    "can_thu_prev": ct_p,
    "can_thu_curr": ct_c,
    "diff_can_thu": diff_ct,
    "diff_can_thu_pct": f"{diff_ct_pct:+0.1f}%",
    "banner_desc": (
        f"• <strong>Tổng quan so sánh 2 tuần:</strong> Tuần W38 phát sinh <strong>{rec_c:,} bản ghi</strong> "
        f"(tăng {diff_rec:+,} đơn, {diff_rec_pct:+0.1f}%) với số tiền ban đầu <strong>{bd_c/1e6:,.1f} Tr ₫</strong> "
        f"({diff_bd_pct:+0.1f}%). Cần truy thu thêm <strong>{ct_c/1e6:,.1f} Tr ₫</strong> "
        f"(tăng {diff_ct/1e6:+,.1f} Tr ₫, {diff_ct_pct:+0.1f}% so với {ct_p/1e6:,.1f} Tr ₫ Tuần W37).<br>"
        "• <strong>Nguyên nhân đột biến:</strong> Phát sinh các vụ <em>Liên đới chiếm dụng</em> (107.6 Tr ₫), "
        "<em>Tick mất hàng</em> (52.0 Tr ₫, tăng +125 đơn), và <em>Kiện thiếu đơn</em> (30.7 Tr ₫).<br>"
        "• <strong>Top AM biến động tiền lớn nhất:</strong> Chị Thái Thị Thanh Thư (+79.9 Tr ₫ do Bắc Nha Trang), "
        "anh Trần Văn Phước (+44.6 Tr ₫ | 678 ticket), chị Huỳnh Thị Kim Chi (+41.4 Tr ₫), anh Nguyễn Ngọc Khánh (+26.1 Tr ₫)."
    )
}

# 2. Comparison by Loại
loai_p = w_prev.groupby('Loại truy thu').agg(don_p=('Mã truy thu', 'count'), bd_p=('ban_dau', 'sum'), ct_p=('can_thu', 'sum'))
loai_c = w_curr.groupby('Loại truy thu').agg(don_c=('Mã truy thu', 'count'), bd_c=('ban_dau', 'sum'), ct_c=('can_thu', 'sum'))
loai_cmp = pd.concat([loai_p, loai_c], axis=1).fillna(0)
loai_cmp['diff_don'] = loai_cmp['don_c'] - loai_cmp['don_p']
loai_cmp['diff_ct'] = loai_cmp['ct_c'] - loai_cmp['ct_p']
loai_cmp = loai_cmp.sort_values('ct_c', ascending=False)

by_loai_list = []
for idx, r in loai_cmp.iterrows():
    loai_name = str(idx)
    don_prev = int(r['don_p'])
    don_curr = int(r['don_c'])
    diff_don = int(r['diff_don'])
    pct_don_diff = f"{round((diff_don / don_prev * 100), 1):+0.1f}%" if don_prev > 0 else ("+100%" if don_curr > 0 else "0%")
    
    ct_prev = float(r['ct_p'])
    ct_curr = float(r['ct_c'])
    diff_ct_val = float(r['diff_ct'])
    pct_ct_diff = f"{round((diff_ct_val / ct_prev * 100), 1):+0.1f}%" if ct_prev > 0 else ("+100%" if ct_curr > 0 else "0%")

    eval_badge = "—"
    if ct_curr >= 20e6 or diff_ct_val >= 20e6:
        eval_badge = "🔴 Tăng mạnh (Bất thường)"
    elif diff_ct_val > 5e6:
        eval_badge = "⚠️ Cảnh báo tăng"
    elif diff_ct_val < -5e6:
        eval_badge = "🟢 Giảm tốt"
    elif ct_curr == 0 and ct_prev == 0:
        eval_badge = "🟢 0 ₫"

    note = ""
    if loai_name == 'Liên đới chiếm dụng':
        note = "Vụ việc Bắc Nha Trang"
    elif loai_name == 'Tick mất hàng':
        note = "Tăng vọt +125 đơn mất hàng"
    elif loai_name == 'Kiện hàng bị thiếu đơn':
        note = "Tăng +96 đơn"
    elif 'Backlog' in loai_name:
        note = "Tồn đọng vận hành"

    by_loai_list.append({
        "loai": loai_name,
        "don_prev": don_prev,
        "don_curr": don_curr,
        "diff_don": diff_don,
        "pct_don_diff": pct_don_diff,
        "can_thu_prev": ct_prev,
        "can_thu_curr": ct_curr,
        "diff_can_thu": diff_ct_val,
        "pct_can_thu_diff": pct_ct_diff,
        "eval": eval_badge,
        "ghi_chu": note
    })

# 3. Comparison by AM
am_p = w_prev.groupby('AM').agg(tk_p=('Mã truy thu', 'count'), bd_p=('ban_dau', 'sum'), ct_p=('can_thu', 'sum'))
am_c = w_curr.groupby('AM').agg(tk_c=('Mã truy thu', 'count'), bd_c=('ban_dau', 'sum'), ct_c=('can_thu', 'sum'))
am_cmp = pd.concat([am_p, am_c], axis=1).fillna(0)
am_cmp['diff_tk'] = am_cmp['tk_c'] - am_cmp['tk_p']
am_cmp['diff_ct'] = am_cmp['ct_c'] - am_cmp['ct_p']
am_cmp = am_cmp.sort_values('ct_c', ascending=False)

am_top_bc = {}
for am_name, grp in w_curr.groupby('AM'):
    bc_sum = grp.groupby('Nơi vi phạm')['can_thu'].sum().sort_values(ascending=False)
    if not bc_sum.empty:
        top_bc_name = bc_sum.index[0]
        top_bc_val = bc_sum.iloc[0]
        am_top_bc[am_name] = f"{top_bc_name} ({top_bc_val/1e6:.1f} Tr)"

by_am_list = []
for idx, r in am_cmp.iterrows():
    am_name = str(idx)
    tk_prev = int(r['tk_p'])
    tk_curr = int(r['tk_c'])
    diff_tk = int(r['diff_tk'])
    pct_tk_diff = f"{round((diff_tk / tk_prev * 100), 1):+0.1f}%" if tk_prev > 0 else ("+100%" if tk_curr > 0 else "0%")

    ct_prev = float(r['ct_p'])
    ct_curr = float(r['ct_c'])
    diff_ct_val = float(r['diff_ct'])
    pct_ct_diff = f"{round((diff_ct_val / ct_prev * 100), 1):+0.1f}%" if ct_prev > 0 else ("+100%" if ct_curr > 0 else "0%")

    level = "🟢 Tốt"
    if ct_curr >= 40e6 or diff_ct_val >= 40e6:
        level = "🔴 Rất cao (≥40 Tr)"
    elif ct_curr >= 15e6 or diff_ct_val >= 15e6:
        level = "🟡 Cần kiểm soát (15-40 Tr)"
    elif tk_curr >= 500:
        level = "⚠️ Nhiều ticket (≥500)"

    by_am_list.append({
        "am": am_name,
        "ticket_prev": tk_prev,
        "ticket_curr": tk_curr,
        "diff_ticket": diff_tk,
        "pct_ticket_diff": pct_tk_diff,
        "can_thu_prev": ct_prev,
        "can_thu_curr": ct_curr,
        "diff_can_thu": diff_ct_val,
        "pct_can_thu_diff": pct_ct_diff,
        "level": level,
        "top_bc_culprit": am_top_bc.get(am_name, "—")
    })

# 4. Comparison by Province
prov_p = w_prev.groupby('Tỉnh').agg(don_p=('Mã truy thu', 'count'), ct_p=('can_thu', 'sum'))
prov_c = w_curr.groupby('Tỉnh').agg(don_c=('Mã truy thu', 'count'), ct_c=('can_thu', 'sum'))
prov_cmp = pd.concat([prov_p, prov_c], axis=1).fillna(0)
prov_cmp['diff_don'] = prov_cmp['don_c'] - prov_cmp['don_p']
prov_cmp['diff_ct'] = prov_cmp['ct_c'] - prov_cmp['ct_p']
prov_cmp = prov_cmp.sort_values('ct_c', ascending=False)

by_province_list = []
for idx, r in prov_cmp.iterrows():
    p_name = str(idx)
    by_province_list.append({
        "tinh": p_name,
        "don_prev": int(r['don_p']),
        "don_curr": int(r['don_c']),
        "diff_don": int(r['diff_don']),
        "can_thu_prev": float(r['ct_p']),
        "can_thu_curr": float(r['ct_c']),
        "diff_can_thu": float(r['diff_ct'])
    })

# 5. Top 30 BC Comparison
bc_p = w_prev.groupby(['Nơi vi phạm', 'AM', 'Tỉnh']).agg(don_p=('Mã truy thu', 'count'), ct_p=('can_thu', 'sum'))
bc_c = w_curr.groupby(['Nơi vi phạm', 'AM', 'Tỉnh']).agg(don_c=('Mã truy thu', 'count'), ct_c=('can_thu', 'sum'))
bc_cmp = pd.concat([bc_p, bc_c], axis=1).fillna(0).reset_index()
bc_cmp['diff_don'] = bc_cmp['don_c'] - bc_cmp['don_p']
bc_cmp['diff_ct'] = bc_cmp['ct_c'] - bc_cmp['ct_p']
bc_cmp = bc_cmp.sort_values('ct_c', ascending=False)

top_bc_list = []
for _, r in bc_cmp.head(30).iterrows():
    ct_p_val = float(r['ct_p'])
    ct_c_val = float(r['ct_c'])
    diff_ct_val = float(r['diff_ct'])
    top_bc_list.append({
        "bc": r['Nơi vi phạm'],
        "am": r['AM'],
        "tinh": r['Tỉnh'],
        "don_prev": int(r['don_p']),
        "don_curr": int(r['don_c']),
        "diff_don": int(r['diff_don']),
        "can_thu_prev": ct_p_val,
        "can_thu_curr": ct_c_val,
        "diff_can_thu": diff_ct_val,
        "pct_can_thu_diff": f"{round((diff_ct_val / ct_p_val * 100), 1):+0.1f}%" if ct_p_val > 0 else ("+100%" if ct_c_val > 0 else "0%")
    })

# Save into data.json and data.js
with open('data.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

d['truy_thu_report'] = {
    "summary": summary,
    "total_records": rec_c,
    "total_ban_dau": bd_c,
    "total_dieu_chinh": dc_c,
    "total_can_thu": ct_c,
    "by_loai": by_loai_list,
    "by_am": by_am_list,
    "by_province": by_province_list,
    "top_bc": top_bc_list
}

with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(d, f, ensure_ascii=False, indent=2)

with open('data.js', 'w', encoding='utf-8') as f:
    f.write('window.DASHBOARD_DATA = ' + json.dumps(d, ensure_ascii=False, indent=2) + ';\n')

print("✅ SUCCESS: Saved 2-Week Truy Thu Comparison into data.json and data.js!")
print(f"Summary: {summary['prev_label']} vs {summary['curr_label']}")
print(f"Total Cần Thu: {ct_p/1e6:.1f} Tr -> {ct_c/1e6:.1f} Tr ({diff_ct/1e6:+.1f} Tr)")
