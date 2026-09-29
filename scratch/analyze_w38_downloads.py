import csv, sys
sys.stdout.reconfigure(encoding='utf-8')

path = r'C:\Users\lap4all\Downloads\w38.csv'

with open(path, 'r', encoding='utf-8', errors='ignore') as f:
    reader = csv.reader(f)
    header = next(reader)
    print("Header:", header)
    
    rows = list(reader)

print(f"Total rows in w38.csv: {len(rows)}")

# Analyze columns
dates = set()
types = {}
places = {}
ams = {}
total_ban_dau = 0
total_can_thu = 0

for r in rows:
    if len(r) < 13:
        continue
    date_val = r[0]
    dates.add(date_val)
    
    # Check column names:
    # 0: Ngày kết luận truy thu, 1: Mã truy thu, 2: Mã ticket, 3: Nhân viên, 4: Chức vụ, 5: Ngày nghỉ việc, 6: Ngày vào làm,
    # 7: ID Nơi vi phạm, 8: Nơi vi phạm, 9: Mã đơn hàng, 10: Loại truy thu, 11: Hình thức truy thu, 12: Số tiền ban đầu, 
    # 13: Điều chỉnh (+|-), 14: Đã thu, 15: Cần thu
    place = r[8] if len(r) > 8 else ''
    loai = r[10] if len(r) > 10 else ''
    ban_dau_str = r[12].replace('.', '').replace(',', '.') if len(r) > 12 else '0'
    can_thu_str = r[15].replace('.', '').replace(',', '.') if len(r) > 15 else (r[14].replace('.', '').replace(',', '.') if len(r) > 14 else '0')
    
    try:
        ban_dau = float(ban_dau_str)
    except:
        ban_dau = 0
    try:
        can_thu = float(can_thu_str)
    except:
        can_thu = 0
        
    total_ban_dau += ban_dau
    total_can_thu += can_thu
    
    types[loai] = types.get(loai, 0) + 1
    places[place] = places.get(place, 0) + 1

print("\nDates in w38.csv:")
for d in sorted(dates):
    print(" ", d)

print(f"\nTotal Ban Dau: {total_ban_dau:,.0f} đ")
print(f"Total Can Thu: {total_can_thu:,.0f} đ")

print("\nTypes count:")
for k, v in sorted(types.items(), key=lambda x: x[1], reverse=True)[:10]:
    print(f"  {k}: {v}")

print("\nTop Places count:")
for k, v in sorted(places.items(), key=lambda x: x[1], reverse=True)[:10]:
    print(f"  {k}: {v}")
