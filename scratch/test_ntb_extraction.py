import pandas as pd
import urllib.request
import os, sys

url = 'https://docs.google.com/spreadsheets/d/1JZ1eRerRqrpwjZ4HBevQunjd8VquM_cvPFz12TaJfMQ/export?format=csv&gid=1301452336'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
df_raw = pd.read_csv(urllib.request.urlopen(req), header=None)

# Find header row
header_row_idx = None
for r_idx in range(len(df_raw)):
    row_vals = [str(x).lower().strip() for x in df_raw.iloc[r_idx].values]
    if any("tổng số lượng" in x or "thời gian cập nhật" in x for x in row_vals):
        continue
    if any(x == "bưu cục" or x == "chi tiết" or x == "tên bc" or "tên bưu cục" in x or "kho_giao_id" in x or "kho_giao_name" in x or "tinh_giao" in x for x in row_vals):
        header_row_idx = r_idx
        break

req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
df_table = pd.read_csv(urllib.request.urlopen(req), skiprows=header_row_idx)
df_table.columns = [str(c).strip() for c in df_table.columns]

def safe_int(val):
    try:
        return int(float(val)) if pd.notna(val) else 0
    except:
        return 0

def parse_unstable_pct(val):
    if pd.isna(val): return 0.0
    val_str = str(val).replace('%', '').strip()
    try:
        f = float(val_str)
        return f if f > 1.0 else f * 100.0
    except:
        return 0.0

def get_val(r, possible_keys, positional_idx=None):
    r_keys = {str(k).strip().lower(): k for k in r.index}
    for pk in possible_keys:
        pk_clean = pk.strip().lower()
        if pk_clean in r_keys:
            val = r[r_keys[pk_clean]]
            if pd.notna(val) and str(val).strip() != "":
                return val
    if positional_idx is not None and positional_idx < len(r):
        val = r.iloc[positional_idx]
        if pd.notna(val) and str(val).strip() != "":
            return val
    return 0

records = []
for _, r in df_table.iterrows():
    po_id = r.iloc[3] # kho_giao_id
    po_name = r.iloc[4] # kho_giao_name
    
    ton_lm = safe_int(get_val(r, ['bl lm', 'ton_lm'], 6))
    ton_lm_5n = safe_int(get_val(r, ['bl lm >5 ngay', 'bl lm > 5 ngay', 'ton_lm_5n'], 7))
    pct_lm_5n = round(parse_unstable_pct(get_val(r, ['%bl lm >5 ngay', '%bl lm > 5 ngay'], 8)), 2)
    ton_ktc = safe_int(get_val(r, ['bl ktc', 'ton_ktc'], 9))
    ton_ktc_cung_tinh = safe_int(get_val(r, ['bl ktc cung tinh', 'bl ktc cung tinh %'], 10))
    pct_ktc_cung_tinh = round(parse_unstable_pct(get_val(r, ['%bl ktc cung tinh'], 11)), 2)
    
    status_val = r.iloc[20] if len(r) > 20 else 'Bình thường'
    reason_val = r.iloc[19] if len(r) > 19 else ''
    days_val = safe_int(r.iloc[17]) if len(r) > 17 else 0
    
    records.append({
        'id': po_id,
        'name': po_name,
        'ton_lm': ton_lm,
        'ton_lm_5n': ton_lm_5n,
        'pct_lm_5n': pct_lm_5n,
        'ton_ktc': ton_ktc,
        'days_unstable': days_val,
        'reason': reason_val,
        'status': status_val
    })

with open('scratch/ntb_extracted.txt', 'w', encoding='utf-8') as f:
    f.write(f"df_raw shape: {df_raw.shape}\n")
    f.write(f"header_row_idx: {header_row_idx}\n")
    f.write(f"df_table columns: {list(df_table.columns)}\n\n")
    f.write("Extracted Records:\n")
    for rec in records[:10]:
        f.write(str(rec) + "\n")

print("Done writing to scratch/ntb_extracted.txt")
