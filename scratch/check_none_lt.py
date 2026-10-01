import os

file_path = r'C:\Users\lap4all\Documents\Auto report\none LT KTC.py'
with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f"Total lines: {len(lines)}")
for i, line in enumerate(lines):
    if 'write_analysis_to_gsheet' in line:
        print(f"Line {i+1}: {line.strip()}")
