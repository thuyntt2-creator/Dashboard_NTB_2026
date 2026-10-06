with open('index.html', 'r', encoding='utf-8') as f:
    for i, line in enumerate(f):
        if 'id="tab-truythu"' in line or 'id="tab-commercial"' in line:
            print(i+1, line.strip())
