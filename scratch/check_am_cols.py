import csv
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

with open('ops_fd.csv', mode='r', encoding='utf-8') as f:
    reader = csv.reader(f)
    lines = list(reader)

print("AM Section Rows (87 to 106):")
for i in range(87, 107):
    line = lines[i]
    print(f"Row {i}: AM={line[0]}, Col6={line[6]}, Col7={line[7]}")
