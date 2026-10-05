import paramiko
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('103.82.27.107', username='root', password='T403kbek9E1r1nJy', timeout=10)

new_run_report = """#!/bin/bash
export PATH="/usr/local/bin:/usr/bin:/bin:$PATH"
cd /root/auto-report
echo "=== CHAY BAO CAO LUC: $(date) ===" >> /root/auto-report/cron.log

# 1. Tải số liệu chuẩn từ Looker Studio và cập nhật tab 'lấy hàng' & 'giao hàng'
python3 autonangsuat.py >> /root/auto-report/cron.log 2>&1

# 2. Gửi báo cáo GTalk theo mốc giờ
CURRENT_HOUR=$(date +%H)
if [ "$CURRENT_HOUR" -eq 14 ]; then
    echo "⏰ [14h00]: Chạy Báo cáo Kết hợp (Target GTC + Năng suất NVPTT)..." >> /root/auto-report/cron.log
    python3 send_realtime_and_target_gtalk.py >> /root/auto-report/cron.log 2>&1
else
    echo "⏰ [${CURRENT_HOUR}h00]: Chạy Báo cáo NĂNG SUẤT NVPTT (Không kèm Target)..." >> /root/auto-report/cron.log
    python3 send_realtime_and_target_gtalk.py --only-nangsuat >> /root/auto-report/cron.log 2>&1
fi
"""

sftp = ssh.open_sftp()
with sftp.file('/root/auto-report/run_report.sh', 'w') as f:
    f.write(new_run_report)
sftp.close()

stdin, stdout, stderr = ssh.exec_command('chmod +x /root/auto-report/run_report.sh && cat /root/auto-report/run_report.sh')
print(stdout.read().decode('utf-8'))
ssh.close()
