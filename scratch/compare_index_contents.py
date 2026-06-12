import difflib

with open("templates/index.html", "r", encoding="utf-8") as f:
    local_lines = f.readlines()

with open("scratch/vercel_index.html", "r", encoding="utf-8") as f:
    vercel_lines = f.readlines()

# Let's clean up dynamic v=... query parameters
import re
def clean_line(l):
    # replace v=19184 with v={{ range(1, 100000) | random }}
    l = re.sub(r'\?v=\d+', '?v={{ range(1, 100000) | random }}', l)
    return l

local_cleaned = [clean_line(l) for l in local_lines]
vercel_cleaned = [clean_line(l) for l in vercel_lines]

diff = difflib.unified_diff(
    local_cleaned,
    vercel_cleaned,
    fromfile="local_index.html",
    tofile="vercel_index.html",
    n=3
)

diff_list = list(diff)
print("Diff lines count:", len(diff_list))

with open("scratch/index_diff_summary.txt", "w", encoding="utf-8") as f:
    f.writelines(diff_list)

print("Saved diff to scratch/index_diff_summary.txt")
