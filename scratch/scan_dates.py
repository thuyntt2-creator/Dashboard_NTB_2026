import os, sys
sys.stdout.reconfigure(encoding='utf-8')

patterns = ['01/08', '12/09', '13/09', '11–17/10', '11-17/10', '18–24/10', '18-24/10', '18/10 – 24/10', '18/10 - 24/10']

files = ['data.json', 'data.js', 'app.js', 'index.html', 'KICH_BAN_THUYET_TRINH_W43_NAM_TRUNG_BO.html', 'KICH_BAN_NOP_COD_QR_VA_TRUY_THU_W43.html']

for fn in files:
    if os.path.exists(fn):
        with open(fn, 'r', encoding='utf-8') as f:
            content = f.read()
        for p in patterns:
            count = content.count(p)
            if count > 0:
                print(f'{fn}: found {count} instances of "{p}"')
