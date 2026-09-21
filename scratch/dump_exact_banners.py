import sys, re
sys.stdout.reconfigure(encoding='utf-8')

content = open('index.html', encoding='utf-8').read()

# Match each exec-banner block up to the closing </div> of exec-banner
# An exec-banner has <div class="exec-banner"...> ... </div> (nested)
# Let's find each <div class="exec-banner" and its full HTML
pos = 0
banner_idx = 1
while True:
    idx = content.find('<div class="exec-banner"', pos)
    if idx == -1:
        break
    # find closing by scanning div tags
    open_tags = 0
    end_idx = idx
    for i in range(idx, len(content)):
        if content[i:i+4] == '<div':
            open_tags += 1
        elif content[i:i+5] == '</div':
            open_tags -= 1
            if open_tags == 0:
                end_idx = i + 6
                break
    banner_html = content[idx:end_idx]
    line_no = content[:idx].count('\n') + 1
    print(f"================ BANNER {banner_idx} (Line {line_no}) ================")
    print(banner_html)
    print("\n")
    pos = end_idx
    banner_idx += 1
