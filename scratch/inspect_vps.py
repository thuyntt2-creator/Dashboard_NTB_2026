import sys, paramiko
sys.stdout.reconfigure(encoding='utf-8')
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('103.82.27.107', username='root', password='T403kbek9E1r1nJy', timeout=10)

stdin, stdout, stderr = ssh.exec_command('grep -n "open(" /root/auto_report/report_nangsuat_direct.py; grep -n "to_csv" /root/auto_report/report_nangsuat_direct.py; grep -n "json.dump" /root/auto_report/report_nangsuat_direct.py')
print("=== SAVING IN VPS ===")
print(stdout.read().decode('utf-8', errors='replace'))

ssh.close()
