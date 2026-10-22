# -*- coding: utf-8 -*-
import sys
import gspread
from google.oauth2.credentials import Credentials

sys.stdout.reconfigure(encoding='utf-8')

creds = Credentials.from_authorized_user_file('authorized_user.json', scopes=['https://www.googleapis.com/auth/spreadsheets'])
gc = gspread.authorize(creds)
sh = gc.open_by_key('14cN4YAf01NqKtREtmhBngRP58OCdgby-PjVoixVlpZo')
ws = sh.worksheet('Kiểm tra')

rows = ws.get('I2:P13')
for r in rows:
    print(r)
