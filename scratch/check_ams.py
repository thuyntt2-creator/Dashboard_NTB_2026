import pandas as pd
import json

df = pd.read_csv('sheet_stuck.csv', encoding='utf-8')
res = {}
for name in ['Đơn Dương', 'Lâm Viên', 'Quảng Tín', 'Đức Trọng', 'Tân Hà', 'Nhân Cơ', 'Tuy Đức']:
    match = df[df['warehouse_name'].str.contains(name, na=False, case=False)]
    res[name] = match[['warehouse_name', 'am_name']].drop_duplicates().to_dict(orient='records')

with open('scratch/check_ams.json', 'w', encoding='utf-8') as f:
    json.dump(res, f, ensure_ascii=False, indent=2)
