import sys
import paramiko

sys.stdout.reconfigure(encoding='utf-8')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('103.82.27.107', username='root', password='T403kbek9E1r1nJy')

print("Starting download_report_gtc_ca1_tts.py on VPS...")
stdin, stdout, stderr = ssh.exec_command('python3 /root/auto-report/download_report_gtc_ca1_tts.py')

while True:
    line = stdout.readline()
    if not line:
        break
    print(line, end='', flush=True)

err = stderr.read().decode('utf-8', errors='replace')
if err:
    print("STDERR:", err)

ssh.close()
