import sys
import pandas as pd

sys.stdout.reconfigure(encoding='utf-8')

# Check structure of sheet_BACKLOG_KTC.csv
with open('sheet_BACKLOG_KTC.csv', 'r', encoding='utf-8', errors='ignore') as f:
    lines = [f.readline() for _ in range(50)]

for i, l in enumerate(lines):
    print(f"Line {i}: {l.strip()[:100]}")
