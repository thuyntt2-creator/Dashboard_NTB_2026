# -*- coding: utf-8 -*-
import sys
import os
import paramiko

sys.stdout.reconfigure(encoding='utf-8')

VPS_IP = '103.82.27.107'
VPS_USER = 'root'
VPS_PASS = 'T403kbek9E1r1nJy'
REMOTE_DIR = '/root/auto-report'

LOCAL_SCRIPT = os.path.join(os.path.dirname(__file__), "send_realtime_and_target_gtalk.py")

def main():
    print(f"Connecting to VPS {VPS_IP}...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(VPS_IP, username=VPS_USER, password=VPS_PASS, timeout=15)

    sftp = ssh.open_sftp()
    remote_script = f"{REMOTE_DIR}/send_realtime_and_target_gtalk.py"
    print(f"Uploading updated {LOCAL_SCRIPT} to {remote_script}...")
    sftp.put(LOCAL_SCRIPT, remote_script)
    print("Upload complete!")

    # Update run_report.sh
    new_run_report = """#!/bin/bash
export PATH="/usr/local/bin:/usr/bin:/bin:$PATH"
cd /root/auto-report
echo "=== CHAY BAO CAO LUC: $(date) ===" >> /root/auto-report/cron.log
python3 fetch_lastmile_productivity.py >> /root/auto-report/cron.log 2>&1

CURRENT_HOUR=$(date +%H)
if [ "$CURRENT_HOUR" -eq 14 ]; then
    echo "⏰ [14h00]: Chạy Báo cáo Kết hợp (Target GTC + Năng suất NVPTT)..." >> /root/auto-report/cron.log
    python3 send_realtime_and_target_gtalk.py >> /root/auto-report/cron.log 2>&1
else
    echo "⏰ [${CURRENT_HOUR}h00]: Chạy Báo cáo NĂNG SUẤT NVPTT (Không kèm Target)..." >> /root/auto-report/cron.log
    python3 send_realtime_and_target_gtalk.py --only-nangsuat >> /root/auto-report/cron.log 2>&1
fi
"""
    with sftp.open(f"{REMOTE_DIR}/run_report.sh", "w") as f:
        f.write(new_run_report.encode("utf-8"))
    print("Updated run_report.sh on VPS!")

    sftp.close()

    # Make run_report.sh executable and check content
    ssh.exec_command(f"chmod +x {REMOTE_DIR}/run_report.sh")
    stdin, stdout, stderr = ssh.exec_command(f"cat {REMOTE_DIR}/run_report.sh")
    print("=== NEW run_report.sh ON VPS ===")
    print(stdout.read().decode('utf-8', errors='replace'))

    # Also test running send_realtime_and_target_gtalk.py --help on VPS to verify --only-nangsuat exists
    stdin, stdout, stderr = ssh.exec_command(f"python3 {REMOTE_DIR}/send_realtime_and_target_gtalk.py --help")
    out = stdout.read().decode('utf-8', errors='replace')
    if "--only-nangsuat" in out:
        print("✅ Flag --only-nangsuat verified on VPS!")
    else:
        print("⚠️ Flag --only-nangsuat NOT found in help!")

    ssh.close()
    print("All done!")

if __name__ == "__main__":
    main()
