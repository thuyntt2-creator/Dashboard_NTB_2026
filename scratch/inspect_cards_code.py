import sys
import paramiko

sys.stdout.reconfigure(encoding='utf-8')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('103.82.27.107', username='root', password='T403kbek9E1r1nJy')

stdin, stdout, stderr = ssh.exec_command("sed -n '880,950p' /root/auto-report/send_realtime_and_target_gtalk.py")
print("=== CARDS & HTML ===")
print(stdout.read().decode('utf-8', errors='replace'))

ssh.close()
