import sys
import paramiko

sys.stdout.reconfigure(encoding='utf-8')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('103.82.27.107', username='root', password='T403kbek9E1r1nJy')

for script in ['download_report_gtc.py', 'download_report_gtc_ca1_tts.py']:
    print(f"\n=== {script} ===")
    stdin, stdout, stderr = ssh.exec_command(f'grep -n -C 8 "cookie" /root/auto-report/{script}')
    print(stdout.read().decode('utf-8', errors='replace'))

ssh.close()
