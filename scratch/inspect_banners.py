import sys
sys.stdout.reconfigure(encoding='utf-8')

tabs = [
    (1008, "tab-gan"),
    (1158, "tab-odr"),
    (1394, "tab-ltc"),
    (1502, "tab-opr-tts"),
    (1652, "tab-rot-lc"),
    (1794, "tab-fd"),
    (2318, "tab-aging"),
    (3329, "tab-bc-canhbao"),
]

with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for start_line, tab_id in tabs:
    print(f"\n===== {tab_id} (around line {start_line}) =====")
    for idx in range(start_line - 1, min(start_line + 40, len(lines))):
        l = lines[idx]
        if 'exec-banner' in l or '<h3' in l or '<p' in l or 'badge-tag' in l or 'id=' in l:
            print(f"{idx+1}: {l.strip()}")
