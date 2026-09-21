import sys
import json
sys.stdout.reconfigure(encoding='utf-8')

with open('data.js', 'r', encoding='utf-8', errors='ignore') as f:
    lines = [f.readline() for _ in range(50)]

print("First 20 lines of data.js:")
for i, l in enumerate(lines[:20]):
    print(f"{i+1}: {l[:100].strip()}")
