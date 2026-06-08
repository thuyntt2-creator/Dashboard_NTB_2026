with open("thu_cung_ky.csv", "r", encoding="utf-8") as f:
    lines = f.readlines()

with open("scratch/inspect_csv_full.txt", "w", encoding="utf-8") as out:
    for idx, line in enumerate(lines):
        out.write(f"Row {idx+1}: {line}")

print(f"Done, wrote {len(lines)} lines.")
