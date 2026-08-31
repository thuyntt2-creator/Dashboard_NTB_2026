with open("app.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "def process_opr" in line or "def get_opr" in line:
        end_idx = i
        for k in range(i+1, len(lines)):
            if lines[k].strip().startswith('def ') and not lines[k].startswith('    '):
                end_idx = k
                break
        print(f"Function in line {i+1} to {end_idx}: {line.strip()}")
        # Write to file
        with open(f"scratch/opr_func_{i+1}.txt", "w", encoding="utf-8") as out:
            out.writelines(lines[i:end_idx])
