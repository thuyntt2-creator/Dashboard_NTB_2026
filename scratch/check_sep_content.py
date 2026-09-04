import sys, re, glob
sys.stdout.reconfigure(encoding='utf-8')

f = glob.glob('scratch/db_s*.html')[0]
with open(f, encoding='utf-8') as file:
    s = file.read()

# Let's find script tags and specific IDs
print("Scripts in db_sếp:")
for m in re.findall(r'<script[^>]*src=[\'"]([^\'"]+)[\'"]', s):
    print(" ", m)

# Let's check some text around footer or header
header_match = re.search(r'<header.*?</header>', s, re.DOTALL)
if header_match:
    print("Header snippet:\n", header_match.group(0)[:500])

# Check some unique titles or text
titles = re.findall(r'<h[1-4][^>]*>(.*?)</h[1-4]>', s)
print("Some headings in sếp:")
for t in titles[:10]:
    print(" ", t)
