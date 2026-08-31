import re

with open("app.py", "r", encoding="utf-8") as f:
    content = f.read()

# Let's find anything that looks like a route or endpoint
matches = re.findall(r'@\w+\.(?:route|get|post)\(["\']([^"\']+)["\']', content)
print("Found routes:")
for m in sorted(list(set(matches))):
    print(" -", m)

# Let's search for "unstable" case-insensitive
unstable_matches = [line for line in content.splitlines() if "unstable" in line.lower()]
print(f"\nFound {len(unstable_matches)} lines with 'unstable':")
for i, line in enumerate(unstable_matches[:20]):
    print(f" {i+1}: {line[:120]}")
