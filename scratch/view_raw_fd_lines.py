import csv
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

with open('ops_fd.csv', mode='r', encoding='utf-8') as f:
    reader = csv.reader(f)
    lines = list(reader)

print(f"Total lines: {len(lines)}")
print("\n--- Header (Line 0) ---")
print(lines[0])

print("\n--- Line 1-5 ---")
for i in range(1, 6):
    print(f"Line {i}: {lines[i]}")

print("\n--- Line 84-90 ---")
for i in range(84, 91):
    print(f"Line {i}: {lines[i]}")

print("\n--- Line 107-115 ---")
for i in range(107, 115):
    print(f"Line {i}: {lines[i]}")
