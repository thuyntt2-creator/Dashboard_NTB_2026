import re

with open("app.py", "r", encoding="utf-8") as f:
    content = f.read()

# Find all route decorator definitions
routes = re.findall(r'@app\.[a-zA-Z_]+\([^\)]+\)', content)
print("Found routes:", len(routes))
for r in routes[:30]:
    print(r)

# Find all occurrences of "def " to see API functions
funcs = [line for line in content.split('\n') if line.strip().startswith('def ')]
print("Total functions:", len(funcs))
with open("scratch/routes_out.txt", "w", encoding="utf-8") as out:
    out.write("=== ROUTES IN APP.PY ===\n")
    for r in routes:
        out.write(r + "\n")
    out.write("\n=== FUNCTIONS IN APP.PY ===\n")
    for fn in funcs:
        out.write(fn + "\n")
