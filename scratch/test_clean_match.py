import sys, os
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from gtalk_ai_bot import ALERT_WID_MAP, fetch_live_gtc_hub, normalize_nfc

def clean_bc_name(name):
    t = normalize_nfc(name).lower()
    for p in ['(ldo)', '(kho)', '(dno)', '(bth)', '(nth)', 'bưu cục']:
        t = t.replace(p, '')
    return t.strip()

def test_find(bc_name, gtc_map):
    nbc = clean_bc_name(bc_name)
    val = 0
    for k, v in gtc_map.items():
        if clean_bc_name(k) == nbc:
            val = v
            break
            
    if val == 0:
        for alert_name, wid in ALERT_WID_MAP.items():
            if clean_bc_name(alert_name) == nbc or (nbc in clean_bc_name(alert_name) and len(nbc) >= 6):
                print(f"⚡ Live API Fetch cho {alert_name} (wid: {wid})...")
                live_gtc = fetch_live_gtc_hub(wid)
                print(f"✅ Kết quả API: {live_gtc} đơn")
                if live_gtc > 0:
                    gtc_map[alert_name] = live_gtc
                    gtc_map[bc_name] = live_gtc
                    return live_gtc
    return val

gtc_map = {'(LDO) Đức Trọng 1': 0, 'Đức Linh': 809}
res = test_find('(LDO) Đức Trọng 1', gtc_map)
print("FINAL RESULT for Đức Trọng 1:", res)
