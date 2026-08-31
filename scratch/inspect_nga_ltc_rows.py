import pickle
import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r"c:\Users\lap4all\Desktop\New folder\scratch\raw_sheets_data.pkl", "rb") as f:
    data = pickle.load(f)

df_raw = data['Theo ngày'].copy()
df_raw['DoanhThu'] = pd.to_numeric(df_raw['DoanhThu'], errors='coerce').fillna(0)
df_raw['Volume'] = pd.to_numeric(df_raw['Volume'], errors='coerce').fillna(0)
df_raw['AM_clean'] = df_raw['AM_format'].astype(str).str.strip()

am_mapping = {
    'Phan Đình Duy': 'Khánh Hòa',
    'Thái Thị Thanh Thư': 'Khánh Hòa',
    'Nguyễn Duy Long': 'Ninh Thuận',
    'Trần Thị Nhung': 'Đắk Nông',
    'Nguyễn Lê Nguyên Vũ': 'Lâm Đồng',
    'Trần Công Hậu': 'Khác',
    'Trần Văn Phước': 'Đắk Nông',
    'Lê Văn Trường': 'Lâm Đồng',
    '': 'Khánh Hòa',
    'Huỳnh Tấn Hiền': 'Bình Thuận',
    'Hồng Bích Nga': 'Lâm Đồng',
    'Phạm Bá Thành Công': 'Khánh Hòa',
    'Huỳnh Thị Kim Chi': 'Lâm Đồng',
    'Trầm Hữu Tiến': 'Lâm Đồng',
    'Nguyễn Ngọc Khánh': 'Bình Thuận',
    'Lê Thanh Nhựt': 'Bình Thuận',
    'Nguyễn Hoàng Phi': 'Khánh Hòa',
    'Lê Minh Đại': 'Lâm Đồng',
    'Phan Đình Duy,Phạm Bá Thành Công': 'Khánh Hòa',
    'Nguyễn Thanh Long': 'Khánh Hòa',
    'Nguyễn Tống Hùng Phong,Thái Thị Thanh Thư,Trần Ngọc Trung': 'Khánh Hòa',
    'Võ Tấn Lợi': 'Lâm Đồng'
}

dates = ['16 thg 6, 2026', '15 thg 6, 2026', '9 thg 6, 2026']

for dt in dates:
    print(f"\n--- DATE: {dt} ---")
    sub = df_raw[df_raw['Ngay'] == dt]
    # Group by clean AM
    gp = sub.groupby('AM_clean').agg(dt_tr=('DoanhThu', lambda x: x.sum() / 1000000.0), vol=('Volume', 'sum')).reset_index()
    # Check each AM's mapping
    for idx, r in gp.iterrows():
        p = am_mapping.get(r['AM_clean'], 'UNMAPPED')
        print(f"  AM: '{r['AM_clean']}' -> Tỉnh in report: {p} | DT: {r['dt_tr']:.2f}M | Vol: {r['vol']:.0f}")
