import sys, os, gspread
from google.oauth2.credentials import Credentials

sys.stdout.reconfigure(encoding='utf-8')
AUTH_FILE = r'C:\Users\lap4all\Documents\Auto report\authorized_user.json'
creds = Credentials.from_authorized_user_file(AUTH_FILE, scopes=['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'])
gc = gspread.authorize(creds)

sh = gc.open_by_key('1-p9VUXndK_7BoiT-a81UfTCbUi953XNmVBoXaTGis_c')
ws_bc = sh.worksheet('BaoCao')
ws_td = sh.worksheet('tự động')

bc_rows = ws_bc.get_all_values()
td_rows = ws_td.get_all_values()

target_bcs = [
    '(BTH) Hàm Liêm', '(BTH) Hàm Thuận', '(BTH) Hàm Thắng', '(BTH) Hàm Tân',
    '(BTH) Liên Hương', '(BTH) Lương Sơn', '(BTH) Phan Rí Cửa', '(BTH) Phú Thủy',
    '(BTH) Phước Hội', '(BTH) Tuyên Quang', '(BTH) Đồng Kho', '(BTH) Đức Linh',
    '(DNO) Cư Jút', '(DNO) Krông Nô', '(DNO) Nhân Cơ 1', '(DNO) ĐL Nam Gia Nghĩa 2'
]

print("=== SO SÁNH TỔNG QUAN GIỮA 2 TAB ===")
for b in target_bcs:
    # Lấy trong BaoCao (Row 4 là header: A=BC, E=Gán, F=TC, H=LTC)
    b_bc = [r for r in bc_rows[4:] if len(r) > 5 and b.lower() in r[0].lower()]
    gan_bc = sum(int(r[4]) for r in b_bc if r[4].replace(',', '').isdigit())
    tc_bc = sum(int(r[5]) for r in b_bc if r[5].replace(',', '').isdigit())

    # Lấy trong tự động
    b_td = [r for r in td_rows[4:] if len(r) > 5 and b.lower() in r[0].lower()]
    gan_td = sum(int(r[4]) for r in b_td if r[4].replace(',', '').isdigit())
    tc_td = sum(int(r[5]) for r in b_td if r[5].replace(',', '').isdigit())

    print(f"{b:<28} | BaoCao: {len(b_bc)} NV, Gán={gan_bc}, TC={tc_bc} | tự động: {len(b_td)} NV, Gán={gan_td}, TC={tc_td}")
