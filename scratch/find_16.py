import os, re, sys
sys.stdout.reconfigure(encoding='utf-8')

for root, dirs, files in os.walk('.'):
    if '.git' in root or 'node_modules' in root or '.gemini' in root:
        continue
    for f in files:
        if f.endswith(('.py', '.html', '.md', '.docx', '.json', '.js')):
            path = os.path.join(root, f)
            try:
                with open(path, 'r', encoding='utf-8', errors='ignore') as fp:
                    content = fp.read()
                matches = re.findall(r'(?:phần|slide|bước|mục)\s*16|16\s*(?:phần|slide|mục)', content, re.IGNORECASE)
                if matches:
                    print(f"File {path} matched: {matches}")
            except Exception:
                pass
