import os, sys
sys.stdout.reconfigure(encoding='utf-8')

print("--- Searching for .xlsx and recent data files ---")
for f in os.listdir('.'):
    if f.endswith('.xlsx') or f.endswith('.xls') or 'qr' in f.lower() or 'ck' in f.lower() or 'chuyen' in f.lower():
        st = os.stat(f)
        print(f"{f:40} | size: {st.st_size} | mtime: {st.st_mtime}")
