import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('data.js', 'r', encoding='utf-8') as f:
    text = f.read()

prefix = "window.DASHBOARD_DATA = "
data = json.loads(text[len(prefix):].rstrip(';\n '))

print("Summary of data keys and sizes:")
for k in [
    'overview', 'san_luong', 'gtc_tong', 'gtc_ca1_thuan', 'gan', 'odr', 'ltc',
    'opr_tts', 'rot_lc', 'fd', 'ktc', 'aging', 'cod_report', 'truy_thu', 'kinh_doanh', 'bc_canh_bao'
]:
    val = data.get(k)
    if isinstance(val, dict):
        print(f"Key '{k}': dict with keys {list(val.keys())[:8]}")
    elif isinstance(val, list):
        print(f"Key '{k}': list with {len(val)} items")
    else:
        print(f"Key '{k}': {type(val)}")
