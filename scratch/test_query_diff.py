# -*- coding: utf-8 -*-
import sys, gspread
from google.oauth2.credentials import Credentials
sys.stdout.reconfigure(encoding='utf-8')
creds = Credentials.from_authorized_user_file('authorized_user.json', scopes=['https://www.googleapis.com/auth/spreadsheets'])
gc = gspread.authorize(creds)
sh_ops = gc.open_by_key('14cN4YAf01NqKtREtmhBngRP58OCdgby-PjVoixVlpZo')
ws_kt = sh_ops.worksheet('Kiểm tra')

for r in range(3, 9):
    l_val = ws_kt.acell(f'L{r}').value
    print(f'Row {r} L{r}: {l_val}')

sh_cb = gc.open_by_key('1lmQv8KwHJzDFs_RMz64ydu4SOmG3M1YAzILNFGtzFec')
ws_lt = sh_cb.worksheet('luu_tru')
lt_vals = ws_lt.get_all_values()
ntb_dates = []
for r in lt_vals[1:]:
    if len(r) > 1 and r[1].strip() == 'NTB':
        d = r[0].strip()
        if d and d not in ntb_dates:
            ntb_dates.append(d)
from datetime import datetime
def parse_date_obj(d_str):
    for fmt in ('%m/%d/%Y', '%d/%m/%Y', '%Y-%m-%d'):
        try: return datetime.strptime(d_str, fmt)
        except ValueError: pass
    return datetime(1970, 1, 1)

sorted_dates = sorted(ntb_dates, key=parse_date_obj)
print('Distinct dates in luu_tru NTB:', [d for d in sorted_dates][-10:])

# Now let's see what Theo dõi BC bể has:
ws_td = sh_ops.worksheet('Theo dõi BC bể')
td_vals = ws_td.get_all_values()
td_dates = []
for r in td_vals[1:]:
    if len(r) > 1:
        d = r[1].strip()
        if d and d not in td_dates:
            td_dates.append(d)
sorted_td_dates = sorted(td_dates, key=parse_date_obj)
print('Distinct dates in Theo dõi BC bể:', [d for d in sorted_td_dates][-10:])
