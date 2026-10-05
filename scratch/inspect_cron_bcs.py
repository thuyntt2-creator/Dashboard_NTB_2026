import sys
import paramiko

sys.stdout.reconfigure(encoding='utf-8')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('103.82.27.107', username='root', password='T403kbek9E1r1nJy')

stdin, stdout, stderr = ssh.exec_command('grep -A 8 -B 2 "Hàm Liêm" /root/auto-report/cron.log')
print("=== HÀM LIÊM IN CRON.LOG ===")
print(stdout.read().decode('utf-8', errors='replace'))

stdin, stdout, stderr = ssh.exec_command('grep -A 8 -B 2 "Đức Linh" /root/auto-report/cron.log')
print("=== ĐỨC LINH IN CRON.LOG ===")
print(stdout.read().decode('utf-8', errors='replace'))

ssh.close()
