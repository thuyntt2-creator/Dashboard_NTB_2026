import json
import sys
import os
import pandas as pd

sys.stdout.reconfigure(encoding='utf-8')

def parse_vn(s):
    try:
        return float(str(s).replace('.', '').replace(',', '.'))
    except:
        return 0.0

print("🚀 Processing sheet_truythu.csv...")
if not os.path.exists('sheet_truythu.csv'):
    print("❌ sheet_truythu.csv not found!")
    sys.exit(1)

tt = pd.read_csv('sheet_truythu.csv', low_memory=False)
print(f"Loaded {len(tt):,} rows from sheet_truythu.csv")

tt['ban_dau']    = tt['Số tiền ban đầu'].apply(parse_vn)
tt['dieu_chinh'] = tt['Điều chỉnh (+|-)'].apply(parse_vn)
tt['can_thu']    = tt['Cần truy thu thêm'].apply(parse_vn)

# Mapping BC -> Tỉnh & AM
bc_map = None
if os.path.exists('sheet_cocau.csv'):
    bc_map = pd.read_csv('sheet_cocau.csv')
elif os.path.exists('co_cau_ntb.csv'):
    bc_map = pd.read_csv('co_cau_ntb.csv')

# AM mapping from Chức vụ = Area Manager / Acting Area Manager
am_rows = tt[tt['Chức vụ'].astype(str).str.contains('Area Manager', na=False)].copy()
am_rows['ten_am'] = am_rows['Nhân viên'].astype(str).apply(lambda x: x.split('-', 1)[1].strip() if '-' in x else x)

bc_am_map = {}
for bc, group in am_rows.groupby('Nơi vi phạm'):
    top_am = group['ten_am'].value_counts().index[0]
    bc_am_map[bc] = top_am

# Tỉnh map
bc_tinh_map = {}
if bc_map is not None:
    cols = bc_map.columns.tolist()
    name_col = next((c for c in cols if 'tên' in c.lower() or 'bưu cục' in c.lower() or 'warehouse' in c.lower()), cols[1])
    prov_col = next((c for c in cols if 'tỉnh' in c.lower() or 'province' in c.lower()), cols[2])
    for _, row in bc_map.iterrows():
        bc_tinh_map[str(row[name_col]).strip()] = str(row[prov_col]).strip()

tt['AM phụ trách'] = tt['Nơi vi phạm'].map(bc_am_map).fillna('—')
tt['Tỉnh/thành phố'] = tt['Nơi vi phạm'].map(bc_tinh_map).fillna('')

EXCL_LOAI = [
    'Backlog Luân Chuyển Trả',
    'Backlog Luân Chuyển Giao',
    'Backlog Bắn Kiểm Giao',
]

# 1. By Loại
by_loai_df = (tt.groupby('Loại truy thu')
           .agg(don=('Mã truy thu', 'count'), bd=('ban_dau', 'sum'),
                dc=('dieu_chinh', 'sum'), ct=('can_thu', 'sum'))
           .sort_values('bd', ascending=False).reset_index())

total_bd = by_loai_df['bd'].sum()
total_don = by_loai_df['don'].sum()
total_dc = by_loai_df['dc'].sum()
total_ct = by_loai_df['ct'].sum()

by_loai_list = []
for _, r in by_loai_df.iterrows():
    loai = r['Loại truy thu']
    p_bd = round((r['bd'] / total_bd * 100) if total_bd else 0, 1)
    p_don = round((r['don'] / total_don * 100) if total_don else 0, 1)
    note = ('⚠️ Giá trị lớn bất thường' if loai == 'Tick mất hàng' else
            '🔴 Nhiều đơn SOP' if loai == 'Khiếu nại/Sai SOP' else
            '🚫 Loại trừ khỏi TOP BC' if loai in EXCL_LOAI else '')
    by_loai_list.append({
        "loai": loai,
        "don": int(r['don']),
        "ban_dau": float(r['bd']),
        "dieu_chinh": float(r['dc']),
        "can_thu": float(r['ct']),
        "pct_tien": p_bd,
        "pct_don": p_don,
        "ghi_chu": note
    })

# 2. Top BC Giao (loại trừ Luân chuyển & Bắn kiểm)
top_bc_giao_df = (tt[~tt['Loại truy thu'].isin(EXCL_LOAI)]
               .groupby(['Nơi vi phạm', 'AM phụ trách', 'Tỉnh/thành phố'])
               .agg(don=('Mã truy thu', 'count'), bd=('ban_dau', 'sum'),
                    dc=('dieu_chinh', 'sum'), ct=('can_thu', 'sum'))
               .sort_values('bd', ascending=False).reset_index().head(25))

top_bc_giao_list = []
for _, r in top_bc_giao_df.iterrows():
    p = round((r['bd'] / total_bd * 100) if total_bd else 0, 1)
    top_bc_giao_list.append({
        "bc": r['Nơi vi phạm'],
        "am": r['AM phụ trách'],
        "tinh": r['Tỉnh/thành phố'],
        "don": int(r['don']),
        "ban_dau": float(r['bd']),
        "dieu_chinh": float(r['dc']),
        "can_thu": float(r['ct']),
        "pct": p
    })

# 3. Top AM theo Ticket
top_am_df = (am_rows.groupby('ten_am')
          .agg(ticket=('Mã truy thu', 'count'), bd=('ban_dau', 'sum'), ct=('can_thu', 'sum'))
          .sort_values('ticket', ascending=False).reset_index())

am_total_ticket = top_am_df['ticket'].sum()
am_total_ct = top_am_df['ct'].sum()
top_am_list = []
for _, r in top_am_df.iterrows():
    p_tk = round((r['ticket'] / am_total_ticket * 100) if am_total_ticket else 0, 1)
    p_ct = round((r['ct'] / am_total_ct * 100) if am_total_ct else 0, 1)
    top_am_list.append({
        "am": r['ten_am'],
        "ticket": int(r['ticket']),
        "pct_ticket": p_tk,
        "ban_dau": float(r['bd']),
        "can_thu": float(r['ct']),
        "pct_tien": p_ct
    })

# 4. Top BC theo Ticket
top_bc_tk_df = (tt.groupby(['Nơi vi phạm', 'AM phụ trách', 'Tỉnh/thành phố'])
                 .agg(ticket=('Mã truy thu', 'count'), bd=('ban_dau', 'sum'), ct=('can_thu', 'sum'))
                 .sort_values('ticket', ascending=False).reset_index().head(30))

bc_tk_total = total_don
top_bc_tk_list = []
for _, r in top_bc_tk_df.iterrows():
    p_tk = round((r['ticket'] / bc_tk_total * 100) if bc_tk_total else 0, 1)
    top_bc_tk_list.append({
        "bc": r['Nơi vi phạm'],
        "am": r['AM phụ trách'],
        "tinh": r['Tỉnh/thành phố'],
        "ticket": int(r['ticket']),
        "pct_ticket": p_tk,
        "can_thu": float(r['ct'])
    })

with open('data.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

d['truy_thu_report'] = {
    "total_records": int(len(tt)),
    "total_ban_dau": float(total_bd),
    "total_dieu_chinh": float(total_dc),
    "total_can_thu": float(total_ct),
    "by_loai": by_loai_list,
    "top_bc_giao": top_bc_giao_list,
    "top_am_ticket": top_am_list,
    "top_bc_ticket": top_bc_tk_list
}

with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(d, f, ensure_ascii=False, indent=2)

with open('data.js', 'w', encoding='utf-8') as f:
    f.write('window.DASHBOARD_DATA = ' + json.dumps(d, ensure_ascii=False, indent=2) + ';\n')

print("✅ SUCCESS: Saved truy_thu_report to data.json & data.js!")
print(f"Tổng đơn: {len(tt):,} | Ban đầu: {total_bd/1e6:,.1f} Tr | Cần thu thêm: {total_ct/1e6:,.1f} Tr")
print(f"Top 1 AM Ticket: {top_am_list[0]['am']} ({top_am_list[0]['ticket']} tickets, {top_am_list[0]['can_thu']/1e6:,.1f} Tr)")
print(f"Top 1 BC Giao: {top_bc_giao_list[0]['bc']} ({top_bc_giao_list[0]['can_thu']/1e6:,.1f} Tr)")
