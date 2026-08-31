with open("app.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "def get_dataframes" in line:
        end_idx = i
        for k in range(i+1, len(lines)):
            if lines[k].strip().startswith('def ') and not lines[k].startswith('    '):
                end_idx = k
                break
        print(f"get_dataframes is from line {i+1} to {end_idx}")
        # Write to file
        with open("scratch/get_dataframes_code.txt", "w", encoding="utf-8") as out:
            out.writelines(lines[i:end_idx])
        break
