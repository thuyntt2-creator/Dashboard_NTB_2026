import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('data.json', encoding='utf-8') as f:
    d = json.load(f)

tt = d.get('truy_thu', {})
ttr = d.get('truy_thu_report', {})

print("truy_thu.overview:", tt.get('overview'))
print("\ntruy_thu_report summary:")
print("  total_records:", ttr.get('total_records'))
print("  total_ban_dau:", f"{ttr.get('total_ban_dau', 0):,.0f}")
print("  total_dieu_chinh:", f"{ttr.get('total_dieu_chinh', 0):,.0f}")
print("  total_can_thu:", f"{ttr.get('total_can_thu', 0):,.0f}")

print("\nBy Loai in truy_thu_report:")
for x in ttr.get('by_loai', [])[:6]:
    print("  ", x['loai'], "| don:", x['don'], "| can_thu:", f"{x['can_thu']:,.0f}")

print("\nTop 5 BC in truy_thu_report (top_bc_giao):")
for x in ttr.get('top_bc_giao', [])[:5]:
    print("  ", x['bc'], "| AM:", x['am'], "| don:", x['don'], "| can_thu:", f"{x['can_thu']:,.0f}")
