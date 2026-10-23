import paramiko
import sys

sys.stdout.reconfigure(encoding='utf-8')
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('103.82.27.107', username='root', password='T403kbek9E1r1nJy')

cmd = """python3 -c "
import sys
sys.path.append('/root/auto_report')
import report_nangsuat_direct as rpt

res = rpt.fetch_all_productivity_direct()
bc_list = []
for am_block in res:
    for bc_name, staff in am_block['bcs']:
        total_gan = sum(int(nv.get('gan', 0)) for nv in staff)
        total_gtc = sum(int(nv.get('tc', 0)) for nv in staff)
        pct = round(total_gtc / total_gan * 100, 1) if total_gan > 0 else 0
        bc_list.append({
            'bc': bc_name,
            'am': am_block['am'],
            'gan': total_gan,
            'gtc': total_gtc,
            'pct': pct
        })

bc_list.sort(key=lambda x: x['pct'])
print('TOTAL BCS:', len(bc_list))
print('=== TOP 10 GTC THAP NHAT REALTIME HOM NAY ===')
for idx, b in enumerate(bc_list[:15], 1):
    print(f'{idx}. {b[\"bc\"]} (AM {b[\"am\"]}) | Gan: {b[\"gan\"]} | GTC: {b[\"gtc\"]} -> {b[\"pct\"]} %')

for b in bc_list:
    if 'Kiến Đức' in b['bc']:
        print('KIEN DUC REALTIME:', b)
"
"""

stdin, stdout, stderr = ssh.exec_command(cmd)
print(stdout.read().decode())
print(stderr.read().decode())
ssh.close()
