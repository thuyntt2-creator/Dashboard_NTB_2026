# -*- coding: utf-8 -*-
import sys
import paramiko

sys.stdout.reconfigure(encoding='utf-8')
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('103.82.27.107', username='root', password='T403kbek9E1r1nJy', timeout=10)

test_code = """
import sys
sys.path.insert(0, '/root/auto_report')
from report_nangsuat_direct import load_alert_hubs_map, FALLBACK_ALERT_HUBS
m = load_alert_hubs_map()
print('--- ALERT HUBS MAP ---')
for k, v in m.items():
    if not k.isdigit():
        print(f'{k}: {v}')
"""

sftp = ssh.open_sftp()
with sftp.file('/root/auto_report/check_map.py', 'w') as f:
    f.write(test_code)
sftp.close()

stdin, stdout, stderr = ssh.exec_command('python3 /root/auto_report/check_map.py')
print(stdout.read().decode('utf-8', errors='replace'))
print('ERR:', stderr.read().decode('utf-8', errors='replace'))

ssh.close()
