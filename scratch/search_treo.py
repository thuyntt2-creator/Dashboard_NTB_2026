with open('app.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

res = []
for i, line in enumerate(lines):
    if 'treo' in line.lower() or '24h' in line.lower():
        res.append(f"{i+1}: {line.strip()[:100]}")

with open('scratch/search_treo_appjs.txt', 'w', encoding='utf-8') as out:
    out.write('\n'.join(res))
