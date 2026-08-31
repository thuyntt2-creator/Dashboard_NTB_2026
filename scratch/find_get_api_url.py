with open("templates/index.html", "r", encoding="utf-8") as f:
    for idx, line in enumerate(f, 1):
        if "getApiUrl" in line and ("function" in line or "=" in line):
            print(f"Line {idx}: {line.strip()}")
