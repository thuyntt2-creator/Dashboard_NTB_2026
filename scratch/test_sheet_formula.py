# -*- coding: utf-8 -*-
import sys, time
import gspread
from google.oauth2.credentials import Credentials

sys.stdout.reconfigure(encoding='utf-8')
creds = Credentials.from_authorized_user_file('authorized_user.json', scopes=['https://www.googleapis.com/auth/spreadsheets'])
gc = gspread.authorize(creds)
sh = gc.open_by_key('14cN4YAf01NqKtREtmhBngRP58OCdgby-PjVoixVlpZo')
ws = sh.worksheet('Kiểm tra')

test_f = "=SUM(QUERY('Data NTB'!A:V, \"SELECT SUM(E) WHERE V = \" & K3 & \" AND D IS NOT NULL GROUP BY D ORDER BY D DESC LIMIT 6 LABEL SUM(E) ''\", 0))"
ws.update(range_name='R3', values=[[test_f]], value_input_option='USER_ENTERED')
time.sleep(2)
print("R3 result (Vol 6d of Duc Trong 1):", ws.acell('R3').value)

test_g = "=SUM(QUERY('Data NTB'!A:V, \"SELECT SUM(J) WHERE V = \" & K3 & \" AND D IS NOT NULL GROUP BY D ORDER BY D DESC LIMIT 6 LABEL SUM(J) ''\", 0))"
ws.update(range_name='S3', values=[[test_g]], value_input_option='USER_ENTERED')
time.sleep(2)
print("S3 result (GTC 6d of Duc Trong 1):", ws.acell('S3').value)
