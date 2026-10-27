with open('scratch/index_with_tab_control.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

start = None
end = None
for i, l in enumerate(lines):
    if '<div class="tab-view" id="tab-control">' in l:
        start = i
    if start is not None and '<div class="tab-view" id="tab-truythu">' in l:
        end = i
        break

print(f"Found tab-control from line {start+1} to {end}")
tab_control_html = "".join(lines[start:end])
with open('scratch/tab_control_extracted.html', 'w', encoding='utf-8') as f:
    f.write(tab_control_html)
print("Saved tab_control_extracted.html!")
