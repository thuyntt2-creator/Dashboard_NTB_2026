with open('app.py', 'r', encoding='utf-8') as f:
    for i, l in enumerate(f, 1):
        if "def index(" in l or "def home(" in l:
            print(f"{i}: {l.strip()}")
