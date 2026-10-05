import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('data.json', encoding='utf-8') as f:
    d = json.load(f)

print("--- 1. GAN AM (Top & Bottom) ---")
for r in d.get('gan_am', []):
    print(f"AM: {r.get('name'):22s} | Vol: {r.get('vol',0):>6} | Ca1+T W39: {r.get('w39_ca1',0):>6}% -> W40: {r.get('w40_ca1',0):>6}% (Δ {r.get('diff_ca1',0):>6}%p) | Tong W40: {r.get('w40',0):>6}% (Δ {r.get('diff',0):>6}%p)")

print("\n--- 2. ODR AM ---")
for r in d.get('odr_am', []):
    print(f"AM: {r.get('name'):22s} | Vol: {r.get('vol',0):>6} | Full W39: {r.get('w39',0):>6}% -> W40: {r.get('w40',0):>6}% (Δ {r.get('diff',0):>6}%p) | TTS W40: {r.get('w40_tts', r.get('tts_w40', 'N/A'))}")

print("\n--- 3. OPR TTS AM ---")
for r in d.get('opr_tts_am', []):
    print(f"AM: {r.get('name'):22s} | Ngay W40: {r.get('w40_day', r.get('day_w40', 'N/A'))} | Dem W40: {r.get('w40_night', r.get('night_w40', 'N/A'))}")

print("\n--- 4. ROT LC AM ---")
for r in d.get('rot_lc_am', []):
    print(f"AM: {r.get('name'):22s} | Vol: {r.get('vol',0):>5} | Rot: {r.get('rot_vol',0):>3} | %Rot W39: {r.get('w39',0):>5}% -> W40: {r.get('w40',0):>5}% (Δ {r.get('diff',0):>5}%p)")

print("\n--- 5. FD AM ---")
for r in d.get('fd_am', []):
    print(f"AM: {r.get('name', r.get('am','')):22s} | Full W40: {r.get('w40_full', r.get('full_w40', 'N/A'))} | TTS W40: {r.get('w40_tts', r.get('tts_w40', 'N/A'))}")

print("\n--- 6. COD REPORT AM ---")
for r in d.get('cod_report', {}).get('am', []):
    print(f"AM: {r.get('am'):22s} | Prev: {r.get('prev_tm')} -> Curr: {r.get('curr_tm')} (Δ {r.get('diff')}) | Muc do: {r.get('level')}")

print("\n--- 7. TRUY THU AM ---")
for r in d.get('truy_thu_report', {}).get('by_am', []):
    print(f"AM: {r.get('am'):22s} | Ticket W40: {r.get('ticket_curr')} | Can thu W40: {r.get('can_thu_curr'):>12,.0f} đ | Culprit: {r.get('top_bc_culprit')}")
