import json, sys

sys.stdout.reconfigure(encoding='utf-8')

with open('data.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

print("=== 1. TOÀN BỘ AM TRONG FD (% HOÀN TRẢ) ===")
for item in d.get('fd', {}).get('am', []):
    stt = item.get('stt')
    am = item.get('am')
    vol = item.get('vol_full', 0)
    ret = item.get('ret_full', 0)
    rate = item.get('rate_full', 0) * 100
    prev = item.get('rate_full_prev', 0) * 100
    diff = item.get('diff_full', 0) * 100
    tts_rate = item.get('rate_tts', 0) * 100
    print(f"STT {stt:2d} | AM: {am:<24} | Vol: {vol:5d} | Hoàn: {ret:4d} | %FD: {rate:5.2f}% (W37: {prev:5.2f}%, Δ: {diff:+5.2f}%p) | TTS FD: {tts_rate:5.2f}%")

print("\n=== 2. TOP 15 BƯU CỤC CÓ %FD CAO NHẤT MẠNG LƯỚI ===")
for item in d.get('fd', {}).get('top_bc', [])[:15]:
    stt = item.get('stt')
    bc = item.get('bc')
    am = item.get('am')
    vol = item.get('vol', 0)
    ret = item.get('ret', 0)
    rate = item.get('rate', 0) * 100
    prev = item.get('rate_prev', 0) * 100
    diff = item.get('diff', 0) * 100
    share = item.get('share_ret', 0) * 100
    print(f"STT {stt:2d} | BC: {bc:<28} | AM: {am:<20} | Giao: {vol:4d} | Hoàn: {ret:3d} | %FD: {rate:5.2f}% (W37: {prev:5.2f}%, Δ: {diff:+5.2f}%p) | Chiếm {share:4.2f}% hoàn toàn vùng")

print("\n=== 3. COD TIỀN MẶT - TỔNG QUAN METRICS ===")
for m in d.get('cod_report', {}).get('metrics', []):
    print(m)

print("\n=== 4. COD TIỀN MẶT - THEO TỪNG AM ===")
for item in d.get('cod_report', {}).get('am_comparison', []):
    stt = item.get('stt')
    am = item.get('am')
    prev = item.get('prev_tm')
    curr = item.get('curr_tm')
    diff = item.get('diff')
    level = item.get('level')
    print(f"STT {stt:>2} | AM: {am:<24} | W37 TM: {prev:>6} | W38 TM: {curr:>6} | Δ: {diff:>7} | Mức độ: {level}")

print("\n=== 5. COD TIỀN MẶT - TOP BƯU CỤC TỶ LỆ TIỀN MẶT CAO NHẤT (VÀ TIỀN MẶT LỚN NHẤT) ===")
for item in d.get('cod_report', {}).get('bc_details', [])[:20]:
    stt = item.get('stt')
    am = item.get('am')
    bc = item.get('bc')
    prev = item.get('prev_tm')
    curr = item.get('curr_tm')
    diff = item.get('diff')
    cash = item.get('cash_m')
    print(f"STT {stt:>2} | BC: {bc:<28} | AM: {am:<20} | %TM: {curr:>6} (W37: {prev:>6}, Δ: {diff:>7}) | Tiền mặt: {cash:>8} Triệu ₫")
