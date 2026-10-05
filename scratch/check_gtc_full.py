import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('data.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

print("=== 5 TỈNH GTC W40 ===")
for r in d.get('gtc_tong', {}).get('tinh', []):
    print(f"{r.get('tinh')}: W39={r.get('w39', 0):.2%}, W40={r.get('w40', 0):.2%}, diff={r.get('diff', 0):.2%}")

print("\n=== 18 AM GTC W40 ===")
for i, r in enumerate(sorted(d.get('gtc_tong', {}).get('am', []), key=lambda x: x.get('w40', 0), reverse=True)):
    print(f"#{i+1}: {r.get('am')} - GTC W40: {r.get('w40', 0):.2%} (W39: {r.get('w39', 0):.2%}), Vol={r.get('vol', 0):,}")
