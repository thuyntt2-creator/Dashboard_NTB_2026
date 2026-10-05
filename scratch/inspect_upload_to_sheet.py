import sys
import paramiko

sys.stdout.reconfigure(encoding='utf-8')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('103.82.27.107', username='root', password='T403kbek9E1r1nJy')

sftp = ssh.open_sftp()
with sftp.open('/root/auto-report/sync_backlog_lm_9h.py', 'r') as f:
    lines = f.readlines()

for i, line in enumerate(lines[100:165], start=101):
    print(f"{i}: {line}", end='')

sftp.close()
ssh.close()
