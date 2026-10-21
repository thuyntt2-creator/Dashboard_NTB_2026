# -*- coding: utf-8 -*-
import sys, paramiko
sys.stdout.reconfigure(encoding='utf-8')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('103.82.27.107', username='root', password='T403kbek9E1r1nJy', timeout=10)

stdin, stdout, stderr = ssh.exec_command('ps aux | grep -E "python|bot|gtalk|ngrok"')
print('=== PROCESSES ON VPS ===')
print(stdout.read().decode('utf-8'))

stdin, stdout, stderr = ssh.exec_command('crontab -l')
print('=== CRONTAB ON VPS ===')
print(stdout.read().decode('utf-8'))

ssh.close()
