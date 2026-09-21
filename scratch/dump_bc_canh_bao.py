import json

with open('data.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

print(f"Total bc_canh_bao: {len(d.get('bc_canh_bao', []))}")
for i, bc in enumerate(d.get('bc_canh_bao', [])):
    print(f"{i+1}. {bc}")
