import paramiko, sys
sys.stdout.reconfigure(encoding='utf-8')
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('103.82.27.107', username='root', password='T403kbek9E1r1nJy')

script = """
import sys
sys.path.append('/root/auto_report')
import report_nangsuat_direct as rpt

alert_map = rpt.load_alert_hubs_map()
data = rpt.fetch_all_productivity_direct()

# Map bc -> total_gtc
bc_gtc = {}
for am_block in data:
    for bc_name, staff in am_block['bcs']:
        norm = rpt.normalize_clean_name(bc_name)
        total_gtc = sum(int(nv.get('GTC', 0)) for nv in staff)
        bc_gtc[norm] = (bc_name, total_gtc, am_block['am'])

print('=== TIẾN ĐỘ THOÁT NHÓM BẤT ỔN HÔM NAY (23/10) ===')
seen = set()
results = []
for k, info in alert_map.items():
    if not isinstance(info, dict) or 'bc_name' not in info: continue
    bc_name = info['bc_name']
    if bc_name in seen: continue
    seen.add(bc_name)
    
    target = info.get('target', 0)
    vol = info.get('vol_today', 0)
    norm = rpt.normalize_clean_name(bc_name)
    
    real_bc_name, gtc, am_name = bc_gtc.get(norm, (bc_name, 0, 'Không rõ'))
    thieu = max(target - gtc, 0)
    pct = round(gtc / target * 100, 1) if target > 0 else 0
    results.append({
        'bc': bc_name,
        'am': am_name,
        'target': target,
        'gtc': gtc,
        'thieu': thieu,
        'pct': pct,
        'vol': vol,
        'is_thoat': target > 0 and gtc >= target
    })

thoat_list = [r for r in results if r['is_thoat']]
chua_list = [r for r in results if not r['is_thoat']]

if thoat_list:
    print('🟢 CÓ', len(thoat_list), 'BƯU CỤC ĐÃ ĐẠT TARGET THOÁT NHÓM HÔM NAY:')
    for r in thoat_list:
        print('•', r['bc'], '(AM ' + r['am'] + '): Đã giao', str(r['gtc']) + '/' + str(r['target']), 'đơn (' + str(r['pct']) + '%) -> 🎉 ĐÃ ĐẠT TARGET THOÁT NHÓM!')
else:
    print('Chưa có bưu cục nào đạt 100% target thoát nhóm hôm nay.')

print('\\n🟡 CÁC BƯU CỤC ĐANG BÁM SÁT TIẾN ĐỘ:')
for r in sorted(chua_list, key=lambda x: x['pct'], reverse=True):
    print('•', r['bc'], '(AM ' + r['am'] + '): Target', r['target'], '| Đã giao', r['gtc'], '-> Còn thiếu', r['thieu'], 'đơn (' + str(r['pct']) + '%)')
"""

stdin, stdout, stderr = ssh.exec_command(f'python3 -c "{script}"')
print(stdout.read().decode('utf-8', errors='ignore'))
print(stderr.read().decode('utf-8', errors='ignore'))
