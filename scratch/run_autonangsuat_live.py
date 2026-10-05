# -*- coding: utf-8 -*-
import paramiko
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('103.82.27.107', username='root', password='T403kbek9E1r1nJy', timeout=10)

print("🚀 Đang khởi chạy autonangsuat.py trên VPS (chỉ tải data, KHÔNG gửi group)...", flush=True)
stdin, stdout, stderr = ssh.exec_command('cd /root/auto-report && python3 -u autonangsuat.py')

for line in iter(stdout.readline, ""):
    print(line, end="", flush=True)

err = stderr.read().decode('utf-8')
if err:
    print("ERR:", err, flush=True)

ssh.close()
