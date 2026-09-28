import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('data.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

print("=== TRUY THU REPORT ===")
ttr = d.get('truy_thu_report', {})
print("Summary:", ttr.get('summary'))
print("\nBy Loai:")
for l in ttr.get('by_loai', []):
    print(" ", l)

print("\nBy AM (Top 5):")
for a in ttr.get('by_am', [])[:6]:
    print(" ", a)

print("\nBy Province:")
for p in ttr.get('by_province', []):
    print(" ", p)

print("\nTop BC Truy Thu:")
for b in ttr.get('top_bc', [])[:6]:
    print(" ", b)

print("\n=== KINH DOANH ===")
kd = d.get('kinh_doanh', {})
print("Total:", kd.get('total'))
print("AM Kinh Doanh:")
for a in kd.get('am', []):
    print(" ", a)

print("\n=== F30 ===")
f30 = d.get('f30', {})
print("Total:", f30.get('total'))
print("AM F30:")
for a in f30.get('am', [])[:5]:
    print(" ", a)

print("\n=== BƯU CỤC CẢNH BÁO ===")
bccb = d.get('bc_canh_bao', [])
print(f"Total BC canh bao: {len(bccb)}")
for b in bccb[:10]:
    print(f"- {b.get('bc')} ({b.get('tinh')} - AM {b.get('am')}): GTC={b.get('gtc_w37')}%, Backlog={b.get('backlog')} don, {b.get('warn_type')}")
