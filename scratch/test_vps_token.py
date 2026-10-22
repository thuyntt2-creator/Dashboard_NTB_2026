# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('103.82.27.107', username='root', password='T403kbek9E1r1nJy', timeout=10)

test_script = """
import requests, json
with open('/root/auto_report/ghn_config.json') as f:
    cfg = json.load(f)
tok = cfg.get('ghn_token', '')
print('Token len:', len(tok))
if not tok.startswith('Bearer '):
    tok = 'Bearer ' + tok
headers = {'Authorization': tok, 'Content-Type': 'application/json'}
payload = {'hub_id': '20320000', 'status': 'ON_TRIP', 'offset': 0, 'limit': 10, 'reverse': 1}
r = requests.post('https://nhanh-api.ghn.vn/api/lastmile/trip/get-trip-list-by-hub', headers=headers, json=payload)
print('Status:', r.status_code)
print('Response:', r.text[:300])
"""

sftp = ssh.open_sftp()
with sftp.file('/root/auto_report/test_token.py', 'w') as f:
    f.write(test_script)
sftp.close()

stdin, stdout, stderr = ssh.exec_command('python3 /root/auto_report/test_token.py')
print(stdout.read().decode('utf-8', errors='replace'))
print('Err:', stderr.read().decode('utf-8', errors='replace'))
ssh.close()
