with open('app.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Extract renderAgingTab (lines ~7885 to 8220)
start_line = -1
for i, l in enumerate(lines):
    if 'function renderAgingTab(' in l:
        start_line = i
        break

print(f"renderAgingTab starts at line {start_line + 1}")

depth = 0
for i in range(start_line, len(lines)):
    l = lines[i]
    # Simple count of { and } ignoring strings/comments
    # We can print when depth returns to 0
    open_c = l.count('{')
    close_c = l.count('}')
    depth += (open_c - close_c)
    if depth == 0:
        print(f"renderAgingTab ends at line {i + 1}")
        break
    if i > start_line + 500:
        print(f"Did not close! Current depth at line {i+1}: {depth}")
        break
