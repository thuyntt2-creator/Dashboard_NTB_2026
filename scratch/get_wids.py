import sys, pandas as pd
sys.stdout.reconfigure(encoding='utf-8')
df = pd.read_csv('co_cau_ntb.csv')
for name in ['Đức Trọng 1', 'Tân Hà', 'Tây Nha Trang', 'Bắc Cam Ranh', 'Lang Biang', 'Quảng Khê', 'Đức An', 'Hòa Ninh', "D'Ran", 'Diên Điền']:
    sub = df[df['Bưu cục'].str.contains(name, case=False, na=False)]
    for _, r in sub.iterrows():
        print(f"{r['Bưu cục']} -> wid: {r['warehouse_id']}")
