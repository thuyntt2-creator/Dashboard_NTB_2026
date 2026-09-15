import json

with open('data.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

t = d.get('treo_lc', {})
with open('scratch/current_treo_data.json', 'w', encoding='utf-8') as out:
    json.dump({
        'total': t.get('total'),
        'total_u24': t.get('total_u24'),
        'total_24_36': t.get('total_24_36'),
        'top_am_sample': t.get('top_am', [])[:3],
        'top_bc_sample': t.get('top_bc', [])[:3]
    }, out, ensure_ascii=False, indent=2)
