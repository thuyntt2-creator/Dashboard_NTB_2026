import sys
import paramiko

sys.stdout.reconfigure(encoding='utf-8')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('103.82.27.107', username='root', password='T403kbek9E1r1nJy')

push_script = """
import sys
import os
import pandas as pd
from datetime import datetime

sys.path.insert(0, '/root/auto-report')
from sync_backlog_lm_9h import _read_excel, _upload_to_sheet, JSON_FILE, SHEET_KEY, SHEET_NAME

TEMP_EXCEL = '/root/auto-report/temp_ghn.xlsx'

print(f"Bắt đầu đọc {TEMP_EXCEL}...")
df = _read_excel(TEMP_EXCEL)
print(f"Tổng số dòng ban đầu: {len(df)}")

EXCLUDED_HUBS = {'1909', '20336000', '20797000', '20745000', '22915000'}
col_bc = None
for col in df.columns:
    if 'bưu cục' in str(col).lower() or 'hub' in str(col).lower() or 'warehouse' in str(col).lower():
        col_bc = col
        break
if col_bc is not None:
    df = df[~df[col_bc].astype(str).str.strip().isin(EXCLUDED_HUBS)].reset_index(drop=True)

total_rows = len(df)
print(f"Đã lọc xong: {total_rows} dòng hợp lệ!")
print(f"Đang đẩy lên Google Sheet '{SHEET_NAME}' (Key: {SHEET_KEY})...")

_upload_to_sheet(JSON_FILE, SHEET_KEY, SHEET_NAME, df)
print(f"🎉 THÀNH CÔNG! Đã cập nhật {total_rows} dòng lên Sheet '{SHEET_NAME}'.")
"""

sftp = ssh.open_sftp()
with sftp.open('/root/auto-report/push_existing_temp.py', 'w') as f:
    f.write(push_script.encode('utf-8'))
sftp.close()

print("Running push_existing_temp.py on VPS...")
stdin, stdout, stderr = ssh.exec_command('python3 /root/auto-report/push_existing_temp.py')
while True:
    line = stdout.readline()
    if not line:
        break
    print(line, end='', flush=True)

err = stderr.read().decode('utf-8', errors='replace')
if err:
    print("STDERR:", err)

ssh.close()
