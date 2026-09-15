with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

res = []
for i, line in enumerate(lines):
    if '11' in line and any(k in line.lower() for k in ['bc', 'bưu', 'cảnh', 'bất ổn', 'backlog']):
        res.append(f"{i+1}: {line.strip()}")

with open('scratch/found_11.txt', 'w', encoding='utf-8') as out:
    out.write('\n'.join(res))
