import sys
import paramiko

sys.stdout.reconfigure(encoding='utf-8')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('103.82.27.107', username='root', password='T403kbek9E1r1nJy')

stdin, stdout, stderr = ssh.exec_command("tail -n 25 /root/auto-report/cron.log")
print("=== CRON.LOG TAIL ===")
print(stdout.read().decode('utf-8', errors='replace'))

stdin, stdout, stderr = ssh.exec_command("grep -n 'GTALK_CHANNEL' /root/auto-report/send_realtime_and_target_gtalk.py")
print("=== GTALK CHANNEL ===")
print(stdout.read().decode('utf-8', errors='replace'))

ssh.close()
