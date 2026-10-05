# -*- coding: utf-8 -*-
import paramiko
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('103.82.27.107', username='root', password='T403kbek9E1r1nJy', timeout=10)

stdin, stdout, stderr = ssh.exec_command('cd /root/auto-report && python3 autonangsuat.py')
for line in iter(stdout.readline, ""):
    print(line, end="")
print("ERR:", stderr.read().decode('utf-8'))
ssh.close()
