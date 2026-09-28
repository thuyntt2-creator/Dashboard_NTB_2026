import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('data.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

bc_list = d.get('gtc_tong', {}).get('bc', [])
print(f"Total bc in gtc_tong: {len(bc_list)}")
targets = ['Lâm Viên', 'Xuân Hương', 'Đức Trọng', 'Quảng Tín', 'Đơn Dương', 'Cam Linh', 'Tây Nha Trang', 'Nhân Cơ', 'Kiến Đức', 'Lang Biang', 'D\'Ran', 'Trường Xuân', 'Đông Gia Nghĩa', 'Bắc Cam Ranh', 'Phú Quý']

for b in bc_list:
    name = b.get('bc', '')
    for t in targets:
        if t.lower() in name.lower():
            rc = b.get('rate_curr', 0) * 100
            rp = b.get('rate_prev', 0) * 100
            diff = b.get('diff', 0) * 100
            print(f"- {name} | AM: {b.get('am')} | Tỉnh: {b.get('tinh')} | W39: {rc:.2f}% | W38: {rp:.2f}% | Diff: {diff:+.2f}%p")
            break
