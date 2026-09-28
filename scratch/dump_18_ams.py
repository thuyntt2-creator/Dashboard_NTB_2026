import sys
import json

sys.stdout.reconfigure(encoding='utf-8')

with open('data.json', encoding='utf-8') as f:
    d = json.load(f)

am_f = {x['am']: x for x in d['san_luong']['am_full']}
am_t = {x['am']: x for x in d['san_luong']['am_tts']}

print(f"{'AM PHỤ TRÁCH':<22} | {'FULL W38':>9} | {'FULL W39':>9} | {'DIFF FULL':>10} | {'TTS W38':>8} | {'TTS W39':>8} | {'DIFF TTS':>9} | {'%TTS':>6}")
print("-" * 95)

for am, f in sorted(am_f.items(), key=lambda x: x[1]['vol'], reverse=True):
    t = am_t.get(am, {})
    f_w38, f_w39, f_diff = f.get('w38', 0), f.get('vol', 0), f.get('diff', 0)
    t_w38, t_w39, t_diff = t.get('w38', 0), t.get('vol', 0), t.get('diff', 0)
    pct_tts = (t_w39 / f_w39 * 100) if f_w39 > 0 else 0
    print(f"{am:<22} | {f_w38:9,d} | {f_w39:9,d} | {f_diff:+10,d} | {t_w38:8,d} | {t_w39:8,d} | {t_diff:+9,d} | {pct_tts:5.1f}%")
