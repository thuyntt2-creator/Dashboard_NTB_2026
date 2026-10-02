import sys
sys.stdout.reconfigure(encoding='utf-8')
import gspread
from google.oauth2.credentials import Credentials

creds = Credentials.from_authorized_user_file('authorized_user.json')
gc = gspread.authorize(creds)
sh = gc.open_by_key('1-p9VUXndK_7BoiT-a81UfTCbUi953XNmVBoXaTGis_c')

# 1. Check cocau for Xuan Huong
ws_cocau = sh.worksheet('cocau')
for r in ws_cocau.get_all_values():
    if 'Xuân Hương' in ' '.join(r) or '21126000' in ' '.join(r):
        print('cocau:', r)

# 2. Check BaoCao for Xuan Huong
ws_bc = sh.worksheet('BaoCao')
bc_vals = ws_bc.get_all_values()
xh_bc = [r for r in bc_vals if len(r) > 0 and 'Xuân Hương' in r[0]]
print(f'BaoCao Xuan Huong rows count: {len(xh_bc)}')
for r in xh_bc:
    print('BaoCao:', r)

# 3. Check RawData for Xuan Huong
ws_raw = sh.worksheet('RawData')
raw_vals = ws_raw.get_all_values()
xh_raw = [r for r in raw_vals if len(r) > 0 and 'Xuân Hương' in r[0]]
print(f'RawData Xuan Huong rows count: {len(xh_raw)}')
for r in xh_raw:
    print('RawData:', r[:6])

# 4. Check 'giao hàng' for Xuan Huong today
ws_gh = sh.worksheet('giao hàng')
gh_vals = ws_gh.get_all_values()
xh_gh = [r for r in gh_vals if len(r) > 2 and 'Xuân Hương' in r[0] and r[2] == '2 thg 10, 2026']
print(f'giao hàng Xuan Huong today rows count: {len(xh_gh)}')
for r in xh_gh:
    print('giao hàng:', r)

# 5. Check 'Data' for Xuan Huong
ws_data = sh.worksheet('Data')
data_vals = ws_data.get_all_values()
xh_data = [r for r in data_vals if len(r) > 16 and ('Xuân Hương' in r[16] or '21126000' in str(r[0]))]
print(f'Data tab Xuan Huong rows count: {len(xh_data)}')
for r in xh_data:
    print('Data tab:', r[0], r[1], r[2], r[6], r[11], r[16], r[17])
