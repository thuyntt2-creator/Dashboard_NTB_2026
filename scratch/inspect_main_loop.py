import sys
import paramiko

sys.stdout.reconfigure(encoding='utf-8')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('103.82.27.107', username='root', password='T403kbek9E1r1nJy')

stdin, stdout, stderr = ssh.exec_command("sed -n '1350,1420p' /root/auto-report/send_realtime_and_target_gtalk.py")
print("=== MAIN LOOP ===")
print(stdout.read().decode('utf-8', errors='replace'))

ssh.close()
