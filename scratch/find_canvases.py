import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

canvases = re.findall(r'<canvas[^>]*id=["\']([^"\']+)["\']', text)
print("All canvas IDs in index.html:")
for c in canvases:
    print(" -", c)
