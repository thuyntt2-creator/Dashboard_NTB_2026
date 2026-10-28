# -*- coding: utf-8 -*-
import sys, os, time
import gspread
from google.oauth2.credentials import Credentials
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')
creds = Credentials.from_authorized_user_file('authorized_user.json', scopes=['https://www.googleapis.com/auth/spreadsheets'])
gc = gspread.authorize(creds)
sh = gc.open_by_key('14cN4YAf01NqKtREtmhBngRP58OCdgby-PjVoixVlpZo')

# 1. Standardize dates in Theo dõi BC bể to YYYY-MM-DD
print("1. Đang chuẩn hóa ngày trong 'Theo dõi BC bể' sang YYYY-MM-DD...")
ws_td = sh.worksheet('Theo dõi BC bể')
all_td = ws_td.get_all_values()
header_td = all_td[0]
rows_td = all_td[1:]

date_col_updates = []
for r in rows_td:
    d_raw = r[1].strip() if len(r) > 1 else ""
    dt = None
    for fmt in ('%d/%m/%Y', '%d/%m/%y', '%Y-%m-%d', '%m/%d/%Y'):
        try:
            dt = datetime.strptime(d_raw, fmt)
            # Ensure year is 2026
            if dt.year < 2000:
                dt = dt.replace(year=2026)
            break
        except:
            pass
    if dt:
        date_col_updates.append([dt.strftime('%Y-%m-%d')])
    else:
        date_col_updates.append([d_raw])

# Update column B in batches
ws_td.update(range_name=f'B2:B{len(date_col_updates)+1}', values=date_col_updates, value_input_option='USER_ENTERED')
print(f"-> Đã chuẩn hóa {len(date_col_updates)} dòng ngày trong 'Theo dõi BC bể'!")

# 2. Extract 27/10/2026 from Data NTB and append to Theo dõi BC bể if not already there
print("\n2. Đang kiểm tra và trích xuất dữ liệu ngày 27/10/2026...")
ws_d = sh.worksheet('Data NTB')
all_d = ws_d.get_all_values()
d27_rows = [r for r in all_d[1:] if len(r) > 3 and '2026-10-27' in r[3]]

# Aggregate by BC name
agg_27 = {}
for r in d27_rows:
    bc = r[1].strip()
    loai = r[2].strip() # 'Hàng Mới Ca 1' or 'Hàng Tồn'
    vol = float(r[4].replace(',', '')) if len(r) > 4 and r[4].replace(',', '').isdigit() else 0
    gtc = float(r[9].replace(',', '')) if len(r) > 9 and r[9].replace(',', '').isdigit() else 0
    gan = float(r[11].replace(',', '')) if len(r) > 11 and r[11].replace(',', '').isdigit() else 0
    chua_gan = float(r[14].replace(',', '')) if len(r) > 14 and r[14].replace(',', '').isdigit() else 0
    
    entry = agg_27.setdefault(bc, {'hang_moi': 0, 'ton_cu': 0, 'gan': 0, 'chua_gan': 0, 'gtc': 0})
    if 'mới' in loai.lower() or 'ca 1' in loai.lower():
        entry['hang_moi'] += vol
    else:
        entry['ton_cu'] += vol
    entry['gan'] += gan
    entry['chua_gan'] += chua_gan
    entry['gtc'] += gtc

rows_to_append = []
for bc, vals in agg_27.items():
    tot_vol = vals['hang_moi'] + vals['ton_cu']
    pct_gtc = f"{(vals['gtc'] / tot_vol * 100):.2f}%" if tot_vol > 0 else "0.00%"
    chua_gtc = max(int(tot_vol - vals['gtc']), 0)
    # Format: ['Bưu cục', 'Ngày', 'Hàng mới về trong ngày', 'Hàng tồn cũ', 'Gán', 'Chưa gán', 'GTC', '%GTC', 'Chưa GTC (Tồn cuối ngày)']
    row_data = [
        bc,
        '2026-10-27',
        str(int(vals['hang_moi'])),
        str(int(vals['ton_cu'])),
        str(int(vals['gan'])),
        str(int(vals['chua_gan'])),
        str(int(vals['gtc'])),
        pct_gtc,
        str(chua_gtc)
    ]
    rows_to_append.append(row_data)

print(f"-> Tạo được {len(rows_to_append)} bưu cục cho ngày 2026-10-27!")

# Check if 2026-10-27 already exists in Theo dõi BC bể
has_27 = any(r[0] == '2026-10-27' for r in date_col_updates)
if not has_27:
    ws_td.append_rows(rows_to_append, value_input_option='USER_ENTERED')
    print("-> Đã nạp thành công 2026-10-27 vào 'Theo dõi BC bể'!")
else:
    print("-> Ngày 2026-10-27 đã có sẵn trong 'Theo dõi BC bể'!")

time.sleep(3)

# 3. Update tab Kiểm tra formulas
print("\n3. Đang cập nhật công thức tab 'Kiểm tra'...")
ws_kt = sh.worksheet('Kiểm tra')

n_formulas = []
for r in range(3, 14):
    f_n = f"=IF(M{r}=0, 0, ROUNDUP(MAX(0.7 * XLOOKUP(K{r}, 'Bất ổn'!$C:$C, 'Bất ổn'!$F:$F) * (SUM(QUERY('Theo dõi BC bể'!$A:$I, \"SELECT C+D WHERE A = '\"&L{r}&\"' ORDER BY B DESC LIMIT 6 LABEL C+D ''\", 0)) + M{r}) - SUM(QUERY('Theo dõi BC bể'!$A:$I, \"SELECT G WHERE A = '\"&L{r}&\"' ORDER BY B DESC LIMIT 6 LABEL G ''\", 0)), 0.50 * (SUM(QUERY('Theo dõi BC bể'!$A:$I, \"SELECT C+D WHERE A = '\"&L{r}&\"' ORDER BY B DESC LIMIT 6 LABEL C+D ''\", 0)) + M{r}) - SUM(QUERY('Theo dõi BC bể'!$A:$I, \"SELECT G WHERE A = '\"&L{r}&\"' ORDER BY B DESC LIMIT 6 LABEL G ''\", 0)), 0.2 * M{r})))"
    n_formulas.append([f_n])

ws_kt.update(range_name='N3:N13', values=n_formulas, value_input_option='USER_ENTERED')

time.sleep(2)

# Check results
print("\n=== KẾT QUẢ CUỐI CÙNG TRÊN GOOGLE SHEET TAB 'KIỂM TRA' ===")
vals_kt = ws_kt.get_values('I2:P9')
for r in vals_kt:
    print(r)
