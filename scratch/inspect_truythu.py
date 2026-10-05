import csv, sys
sys.stdout.reconfigure(encoding='utf-8')

print("--- SHEET TRUYTHU HEAD ---")
try:
    with open('sheet_truythu.csv', encoding='utf-8', errors='ignore') as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader):
            if i < 10:
                print(f"Row {i}:", row[:10])
            else:
                break
except Exception as e:
    print("Error reading sheet_truythu.csv:", e)
