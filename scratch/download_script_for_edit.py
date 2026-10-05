import sys
import paramiko

sys.stdout.reconfigure(encoding='utf-8')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('103.82.27.107', username='root', password='T403kbek9E1r1nJy')

sftp = ssh.open_sftp()
sftp.get('/root/auto-report/send_realtime_and_target_gtalk.py', 'scratch/send_realtime_and_target_gtalk.py')
print("Downloaded send_realtime_and_target_gtalk.py to scratch.")

sftp.close()
ssh.close()
