import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

def find_snippet(kw, length=500):
    idx = text.find(kw)
    if idx != -1:
        print(f"=== Snippet for {kw} ===")
        print(text[idx-50:idx+length])
    else:
        print(f"Not found: {kw}")

find_snippet('table-gtc-tts-ca1-detailed', 600)
find_snippet('table-vol-tinh-full', 600)
find_snippet('table-gtc-tinh-full', 600)
find_snippet('table-gan-overview-region', 600)
find_snippet('table-odr-tinh-full', 600)
find_snippet('table-rot-am-detailed', 600)
