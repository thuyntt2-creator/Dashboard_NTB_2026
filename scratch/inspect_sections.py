with open(r'c:\Users\lap4all\Desktop\New folder\scratch\generate_professional_w38_script.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for idx, line in enumerate(lines):
    if 'add_speech_section' in line or 'sec_title=' in line or 'VIII' in line or 'OPR' in line or 'opr' in line:
        print(f"Line {idx+1}: {line.strip()}")
