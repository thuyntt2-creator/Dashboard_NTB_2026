import os

targets = [
    r'c:\Users\lap4all\Desktop\New folder\report_target_gtalk.py',
    r'c:\Users\lap4all\Desktop\New folder\push_off_tuyen_am.py',
    r'c:\Users\lap4all\Desktop\New folder\push_don_tts_am.py',
    r'c:\Users\lap4all\Desktop\New folder\pushtreolc.py',
    r'c:\Users\lap4all\Desktop\auto-report\report_target_gtalk.py',
    r'c:\Users\lap4all\Desktop\auto-report\send_realtime_and_target_gtalk.py',
    r'c:\Users\lap4all\Desktop\auto-report\send_realtime_productivity_gtalk.py'
]

am_entry = '    "Phan Nguyễn Yến Nhi": "2105595062412402688",\n'

for p in targets:
    if not os.path.exists(p):
        print(f"Skipping not found: {p}")
        continue
    with open(p, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    if "Phan Nguyễn Yến Nhi" in content:
        print(f"Already present in: {p}")
        continue
        
    # Find "Nguyễn Đỗ Minh Nghĩa": "2100062122691026944"
    target_str = '"Nguyễn Đỗ Minh Nghĩa": "2100062122691026944"'
    if target_str in content:
        idx = content.find(target_str)
        # find end of line
        eol = content.find('\n', idx)
        if eol != -1:
            # check if line ends with comma
            line = content[idx:eol]
            if not line.strip().endswith(','):
                # add comma
                content = content[:idx] + line + ',' + content[eol:]
                eol += 1
            content = content[:eol+1] + am_entry + content[eol+1:]
            with open(p, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Updated: {p}")
    else:
        print(f"Could not find anchor in: {p}")
