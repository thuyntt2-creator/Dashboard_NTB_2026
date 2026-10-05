import csv, sys
sys.stdout.reconfigure(encoding='utf-8')

print("--- SHEET AGING HEAD ---")
try:
    with open('sheet_aging.csv', encoding='utf-8', errors='ignore') as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader):
            if i < 5:
                print(f"Row {i}:", row[:10])
            else:
                break
except Exception as e:
    print("Error:", e)

print("\n--- TRUY THU SUMMARY ---")
total_truythu = 0
total_da_truythu = 0
total_can_truythu = 0
by_am = {}
by_type = {}

with open('sheet_truythu.csv', encoding='utf-8', errors='ignore') as f:
    reader = csv.DictReader(f)
    for r in reader:
        try:
            ban_dau = float(r.get('Số tiền ban đầu', 0) or 0)
            da_tt = float(r.get('Đã truy thu', 0) or 0)
            can_tt = float(r.get('Cần truy thu thêm', 0) or 0)
            total_truythu += ban_dau
            total_da_truythu += da_tt
            total_can_truythu += can_tt
            
            nv = r.get('Nhân viên', 'Khác')
            loai = r.get('Loại truy thu', 'Khác')
            by_am[nv] = by_am.get(nv, 0) + ban_dau
            by_type[loai] = by_type.get(loai, 0) + ban_dau
        except:
            pass

print(f"Tổng số tiền truy thu ban đầu: {total_truythu:,.0f} đ")
print(f"Đã truy thu: {total_da_truythu:,.0f} đ")
print(f"Cần truy thu thêm: {total_can_truythu:,.0f} đ")

print("\nTop loại truy thu:")
for k, v in sorted(by_type.items(), key=lambda x: x[1], reverse=True)[:5]:
    print(f"- {k}: {v:,.0f} đ")

print("\nTop nhân sự / AM bị truy thu nhiều nhất:")
for k, v in sorted(by_am.items(), key=lambda x: x[1], reverse=True)[:10]:
    print(f"- {k}: {v:,.0f} đ")
