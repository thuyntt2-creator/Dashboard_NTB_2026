import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('data.js', 'r', encoding='utf-8') as f:
    text = f.read()

prefix = "window.DASHBOARD_DATA = "
data = json.loads(text[len(prefix):].rstrip(';\n '))

print("=== 1. OVERVIEW ===")
cards = data['overview'].get('cards', {})
print("Cards:", json.dumps(cards, ensure_ascii=False, indent=2))

print("\n=== 4. GTC CA1 TTS ===")
print("GTC CA1:", json.dumps(data.get('gtc_ca1_thuan', {}).get('overview', {}), ensure_ascii=False))

print("\n=== 5. GAN ===")
print("GAN overview:", json.dumps(data.get('gan', {}).get('overview', {}), ensure_ascii=False))

print("\n=== 8. OPR TTS ===")
print("OPR TTS keys:", list(data.get('opr_tts', {}).keys()))
if 'tinh' in data.get('opr_tts', {}):
    print("OPR TTS tinh:", json.dumps(data['opr_tts']['tinh'][:3], ensure_ascii=False))

print("\n=== 9. ROT LC ===")
print("ROT LC overview:", json.dumps(data.get('rot_lc', {}).get('overview', {}), ensure_ascii=False))
print("ROT LC top bc:", json.dumps(data.get('rot_lc', {}).get('top_bc', [])[:3], ensure_ascii=False))

print("\n=== 10. FD ===")
print("FD overview:", json.dumps(data.get('fd', {}).get('overview', {}), ensure_ascii=False))
print("FD top bc:", json.dumps(data.get('fd', {}).get('top_bc', [])[:3], ensure_ascii=False))

print("\n=== 11. KTC ===")
ktc = data.get('ktc', {})
print("Fill rate:", json.dumps(ktc.get('fill_rate', {}).get('overview', {}), ensure_ascii=False))
print("Backlog:", json.dumps(ktc.get('backlog', {}).get('overview', {}), ensure_ascii=False))

print("\n=== 12. AGING ===")
aging = data.get('aging', {})
print(f"Total: {aging.get('total')}, 5-8: {aging.get('total_5_8')}, 8-15: {aging.get('total_8_15')}, >15: {aging.get('total_gt_15')}")
print("Top BC aging:", json.dumps(aging.get('top_bc', [])[:3], ensure_ascii=False))

print("\n=== 13. COD REPORT ===")
cod = data.get('cod_report', {})
print("COD metrics:", json.dumps(cod.get('metrics', {}), ensure_ascii=False))
print("COD summary_text:", cod.get('summary_text', ''))

print("\n=== 14. TRUY THU ===")
tt = data.get('truy_thu', {})
print("Truy thu overview:", json.dumps(tt.get('overview', {}), ensure_ascii=False))
print("Truy thu types:", json.dumps(tt.get('types', []), ensure_ascii=False))

print("\n=== 15. KINH DOANH ===")
kd = data.get('kinh_doanh', {})
print("KD total:", json.dumps(kd.get('total', {}), ensure_ascii=False))
f30 = data.get('f30', {})
print("F30 total:", json.dumps(f30.get('total', {}), ensure_ascii=False))

print("\n=== 16. BC CANH BAO ===")
bccb = data.get('bc_canh_bao', [])
print(f"Total BC canh bao: {len(bccb)}")
for b in bccb[:5]:
    print(f"  {b.get('bc') or b.get('bưu cục')}: GTC={b.get('gtc')}, Backlog={b.get('backlog')}")
