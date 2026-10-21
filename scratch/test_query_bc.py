import sys, gspread, time
sys.stdout.reconfigure(encoding='utf-8')
from google.oauth2.credentials import Credentials

creds = Credentials.from_authorized_user_file('authorized_user.json', ['https://www.googleapis.com/auth/spreadsheets'])
gc = gspread.authorize(creds)
sh = gc.open_by_key('14cN4YAf01NqKtREtmhBngRP58OCdgby-PjVoixVlpZo')
ws = sh.worksheet('Kiểm tra')

ws.update(range_name='Z1', values=[['=QUERY(\'Theo dõi BC bể\'!A:I, "SELECT B, C+D, G WHERE A = \'(KHO) Tây Nha Trang\' ORDER BY B DESC LIMIT 6", 0)']])
time.sleep(2)
res = ws.get_values('Z1:AB7')
print('QUERY ORDER BY B DESC LIMIT 6 returned:')
for r in res:
    print(r)
ws.batch_clear(['Z1:AB7'])
