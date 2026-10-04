# -*- coding: utf-8 -*-
import sys
import paramiko

sys.stdout.reconfigure(encoding='utf-8')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('103.82.27.107', username='root', password='T403kbek9E1r1nJy', timeout=10)

# 1. Tạo script run_report.sh
script_content = """#!/bin/bash
export PATH="/usr/local/bin:/usr/bin:/bin:$PATH"
cd /root/auto-report
echo "=== CHAY BAO CAO LUC: $(date) ===" >> /root/auto-report/cron.log
python3 fetch_lastmile_productivity.py >> /root/auto-report/cron.log 2>&1
python3 send_realtime_and_target_gtalk.py >> /root/auto-report/cron.log 2>&1
"""

sftp = ssh.open_sftp()
with sftp.file('/root/auto-report/run_report.sh', 'w') as f:
    f.write(script_content)
sftp.close()

ssh.exec_command('chmod +x /root/auto-report/run_report.sh')

# 2. Cài đặt Crontab theo giờ VN
cron_lines = "0 14,16,18,20,21 * * * /root/auto-report/run_report.sh\n"
ssh.exec_command('echo "' + cron_lines.strip() + '" | crontab -')

_, stdout, _ = ssh.exec_command('crontab -l')
print("✅ Lịch Crontab tự động trên VPS:")
print(stdout.read().decode())

ssh.close()
