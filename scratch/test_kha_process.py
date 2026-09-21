import gspread
import pandas as pd
import json

gc = gspread.oauth(authorized_user_filename='authorized_user.json')
doc = gc.open_by_key('1E9BdaxouCeTUBeGLh0kyieyWE6wZoymglbZw19LRKEo')

ws_kha = doc.worksheet('KH A')
vals_kha = ws_kha.get_all_values()
df_kha = pd.DataFrame(vals_kha[1:], columns=vals_kha[0])

# Clean dates
def parse_date_str(d):
    import re
    m = re.search(r'(\d+)\s+thg\s+(\d+)', str(d))
    if m:
        return f"{int(m.group(1)):02d}/{int(m.group(2)):02d}"
    return str(d)

df_kha['clean_date'] = df_kha['Ngay'].apply(parse_date_str)
df_kha['DT_num'] = pd.to_numeric(df_kha['DT'], errors='coerce').fillna(0)

# Get September dates in chronological order
all_dates = sorted(
    [d for d in df_kha['clean_date'].unique() if '/09' in d],
    key=lambda x: int(x.split('/')[0])
)
print("September dates in KH A:", all_dates)

# Map shop AM and buu cuc
SHOP_META = {
    "3200594": {"am": "Lê Thanh Nhựt", "buu_cuc": "2357 - (BTH) Đồng Kho"},
    "3559462": {"am": "Nguyễn Lê Nguyên Vũ", "buu_cuc": "20663000 - (LDO) Đạ Tẻh"},
    "3910354": {"am": "Phan Đình Duy", "buu_cuc": "20495000 - (KHO) Nha Trang"},
    "3950975": {"am": "Phan Đình Duy", "buu_cuc": "21046000 - (KHO) Vạn Ninh"},
    "4264387": {"am": "Huỳnh Thúc Duân", "buu_cuc": "22242000 - (DNO) Bắc Gia Nghĩa"},
    "4313038": {"am": "Hồng Bích Nga", "buu_cuc": "20785000 - (LDO) B'Lao"},
    "5099749": {"am": "Thái Thị Thanh Thư", "buu_cuc": "22363000 - (KHO) Nam Nha Trang 3"},
    "5109892": {"am": "Lê Văn Trường", "buu_cuc": "22116000 - (LDO) Xuân Trường - Đà Lạt"},
    "5197975": {"am": "Nguyễn Duy Long", "buu_cuc": "20499000 - (NTH) Phước Dinh"},
    "5212344": {"am": "Huỳnh Thúc Duân", "buu_cuc": "22242000 - (DNO) Bắc Gia Nghĩa"}
}

for makh, g in df_kha.groupby('MaKH'):
    meta = SHOP_META.get(str(makh), {})
    last_r = g.iloc[-1]
    print(f"Shop: {makh} - {last_r['TenKH']} | AM: {meta.get('am')} | MTD: {last_r['MTD']} | Trụ hạng: {last_r['%Trụ hạng']} | Rows: {len(g)}")
