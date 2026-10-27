import re, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx1 = text.find('id="tab-truythu"')
idx2 = text.find('id="tab-commercial"')
tab_tt = text[idx1:idx2]

dates = re.findall(r'\d{1,2}[\/\-–]\d{1,2}', tab_tt)
print('Dates in tab-truythu:', set(dates))
for line in tab_tt.splitlines():
    if any(k in line for k in ['12/10', '18/10', '19/10', '25/10', '11/10', '17/10', '01/08', '12/09', '13/09']):
        print(line.strip())
