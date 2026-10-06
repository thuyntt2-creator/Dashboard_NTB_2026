import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('data.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

t = d.get('treo_lc', {})
am_stuck = t.get('top_am', [])
print('Sorted by VOL (Total Luân chuyển):')
for x in am_stuck[:6]:
    print(f"- AM {x['am']} ({x['tinh']}): Total={x['vol']}, <24h={x['u_24']}, Treo>=24h={x['treo_24']}, Treo>=36h={x['treo_36']}")

print('\nSorted by TREO >= 24h (Thực tế tồn đọng trễ luân chuyển):')
by_treo24 = sorted(am_stuck, key=lambda x: x['treo_24'], reverse=True)
for x in by_treo24[:6]:
    print(f"- AM {x['am']} ({x['tinh']}): Treo>=24h={x['treo_24']}, Treo>=36h={x['treo_36']}, Total={x['vol']}, <24h={x['u_24']}")

print('\nTop BC sorted by VOL vs sorted by TREO >= 24h:')
bc_stuck = t.get('top_bc', [])
print('Top BC by vol:')
for x in bc_stuck[:5]:
    print(f"- BC {x['bc']} ({x['am']}): Total={x['vol']}, Treo>=24h={x['treo_24']}, Treo>=36h={x['treo_36']}")

print('\nTop BC by Treo>=24h:')
by_bc_treo = sorted(bc_stuck, key=lambda x: x['treo_24'], reverse=True)
for x in by_bc_treo[:5]:
    print(f"- BC {x['bc']} ({x['am']}): Treo>=24h={x['treo_24']}, Treo>=36h={x['treo_36']}, Total={x['vol']}")
