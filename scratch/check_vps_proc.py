import paramiko
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('103.82.27.107', username='root', password='T403kbek9E1r1nJy', timeout=10)
stdin, stdout, stderr = ssh.exec_command('ps aux | grep python3')
for line in stdout.read().decode('utf-8').split('\n'):
    if any(k in line for k in ['send_realtime', 'run_report', 'autonangsuat', 'fetch_lastmile']):
        print('FOUND PROCESS:', line)
print('Crontab currently:')
stdin, stdout, stderr = ssh.exec_command('crontab -l')
print(stdout.read().decode('utf-8'))
ssh.close()
