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
from report_nangsuat_direct import load_alert_hubs_map, find_alert_info, build_push_bat_on_message

alert_map = load_alert_hubs_map()

test_cases = [
    ('Lê Văn Trường', '(LDO) Lang Biang - Đà Lạt 2', 450),
    ('Lê Văn Trường', "(LDO) D'Ran", 120),
    ('Huỳnh Thị Kim Chi', '(LDO) Tân Hà Lâm Hà', 250),
    ('Lê Minh Lợi', '(LDO) Lang Biang - Đà Lạt 1', 200),
    ('Hồng Bích Nga', '(LDO) Hòa Ninh', 400),
]

for am, bc, gtc in test_cases:
    info = find_alert_info(bc, alert_map)
    msg = build_push_bat_on_message(am, bc, info, gtc)
    print('==============================')
    print(f'BC: {bc} | Target: {info.get("target")} | Vol: {info.get("vol_today")}')
    print(msg)
"""

sftp = ssh.open_sftp()
with sftp.file('/root/auto_report/test_msgs.py', 'w') as f:
    f.write(test_code)
sftp.close()

stdin, stdout, stderr = ssh.exec_command('python3 /root/auto_report/test_msgs.py')
print(stdout.read().decode('utf-8', errors='replace'))

ssh.close()
