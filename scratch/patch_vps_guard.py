# -*- coding: utf-8 -*-
import sys
import paramiko

sys.stdout.reconfigure(encoding='utf-8')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('103.82.27.107', username='root', password='T403kbek9E1r1nJy', timeout=10)

patch_script = """
import re
from datetime import datetime, timedelta

# Patch calculate_and_render_report.py
fpath = '/root/auto-report/calculate_and_render_report.py'
with open(fpath, 'r', encoding='utf-8') as f:
    code = f.read()

# Kiểm tra nếu chưa có guard
guard_code = '''
    # CHỐT CHẶN AN TOÀN: Kiểm tra ngày mới nhất có phải là ngày hôm qua (N-1) không
    from datetime import datetime, timedelta
    yesterday = datetime.now() - timedelta(days=1)
    yesterday_str = yesterday.strftime('%Y-%m-%d')
    if yesterday_str not in latest_date:
        print(f"⚠️ [CHỐT CHẶN AN TOÀN]: Ngày mới nhất trên Sheet là '{latest_date}', không phải ngày hôm qua ({yesterday_str})!")
        print("❌ Dừng gửi báo cáo để tránh gửi nhầm số liệu ngày cũ lên GTalk!")
        return
'''

if 'CHỐT CHẶN AN TOÀN' not in code:
    target = 'print(f"-> Mốc ngày mới nhất: {latest_date}")'
    if target in code:
        code = code.replace(target, target + guard_code)
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(code)
        print("✅ Đã cài chốt chặn an toàn cho calculate_and_render_report.py")

# Patch report_gtc_ca1_tts.py
fpath2 = '/root/auto-report/report_gtc_ca1_tts.py'
with open(fpath2, 'r', encoding='utf-8') as f:
    code2 = f.read()

guard_code2 = '''
    # CHỐT CHẶN AN TOÀN: Kiểm tra Target Date có phải là ngày hôm qua (N-1) không
    from datetime import datetime, timedelta
    yesterday_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    if target_date != yesterday_date:
        print(f"⚠️ [CHỐT CHẶN AN TOÀN]: Target date trên Sheet là '{target_date}', không phải ngày hôm qua ({yesterday_date})!")
        print("❌ Dừng gửi báo cáo để tránh gửi nhầm số liệu ngày cũ lên GTalk!")
        return
'''

if 'CHỐT CHẶN AN TOÀN' not in code2:
    target2 = 'print(f"📅 Target Date (N-1): {target_date} (Hiển thị: {display_date})")'
    if target2 in code2:
        code2 = code2.replace(target2, target2 + guard_code2)
        with open(fpath2, 'w', encoding='utf-8') as f:
            f.write(code2)
        print("✅ Đã cài chốt chặn an toàn cho report_gtc_ca1_tts.py")
"""

sftp = ssh.open_sftp()
with sftp.file('/root/auto-report/apply_safety_guard.py', 'w') as f:
    f.write(patch_script)
sftp.close()

_, stdout, _ = ssh.exec_command('python3 /root/auto-report/apply_safety_guard.py')
print(stdout.read().decode())

ssh.close()
