import re

with open("templates/index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Find the section containing backlog table rendering
# We can search for 'chua_giao' or 'aging' related Javascript
matches = re.finditer(r"function\s+renderAging\w*|renderAgingTable|populateAging", html, re.IGNORECASE)
out = []
for m in matches:
    start = max(0, m.start() - 200)
    end = min(len(html), m.end() + 2000)
    out.append(f"--- MATCH AT {m.start()} ---")
    out.append(html[start:end])
    out.append("-" * 50)

with open("scratch/search_backlog_table_res.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print("Results saved to scratch/search_backlog_table_res.txt")
