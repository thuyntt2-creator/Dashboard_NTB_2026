import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('data.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

fd = d.get('fd', {})
print("=== OVERVIEW ===")
print("overview:", json.dumps(fd.get('overview', {}), ensure_ascii=False))
print("summary:", json.dumps(fd.get('summary', {}), ensure_ascii=False))

print("\n=== ALL AMs (SORTED BY STT) ===")
for a in fd.get('am', []):
    stt = a.get('stt')
    am = a.get('am')
    code = a.get('am_code')
    vf = a.get('vol_full', 0)
    rf = a.get('ret_full', 0)
    rate_f = a.get('rate_full', 0) * 100
    prev_f = a.get('rate_full_prev', 0) * 100
    diff_f = a.get('diff_full', 0) * 100
    
    vt = a.get('vol_tts', 0)
    rt = a.get('ret_tts', 0)
    rate_t = a.get('rate_tts', 0) * 100
    diff_t = a.get('diff_tts', 0) * 100
    
    print(f"{stt}. {am} ({code}): Full Vol={vf}, Hoàn={rf} ({rate_f:.2f}%, W38: {prev_f:.2f}%, Diff: {diff_f:+.2f}%p) -- TTS Vol={vt}, Hoàn={rt} ({rate_t:.2f}%, Diff: {diff_t:+.2f}%p)")

print("\n=== TOP BC HOÀN CAO NHẤT ===")
for b in fd.get('top_bc', [])[:15]:
    print(f"- {b.get('bc')} (AM {b.get('am')}): Full Vol={b.get('vol_full')}, Hoàn={b.get('ret_full')} ({b.get('rate_full', 0)*100:.2f}%) -- TTS: {b.get('rate_tts', 0)*100:.2f}%")
