import os
import sys
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import report_BC_canh_bao_gtalk as rpt

cb_items, update_time, n1_comp = rpt.load_data()
print(f"Total alert hubs: {len(cb_items)}")
for it in cb_items:
    print(f"BC: {it['bc_name']} | AM: {it['am']} | Vol: {it['vol_today']} | Target: {it['req_gtc']} | Achievable: {it['is_achievable']}")
