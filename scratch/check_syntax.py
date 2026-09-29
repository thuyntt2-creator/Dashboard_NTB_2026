import re

with open('app.js', encoding='utf-8') as f:
    text = f.read()

# Remove comments
# 1. Block comments
text = re.sub(r'/\*[\s\S]*?\*/', '', text)
# 2. Line comments
text = re.sub(r'//.*', '', text)

stack = []
in_str = None
esc = False
line = 1

for i, ch in enumerate(text):
    if ch == '\n':
        line += 1
    if esc:
        esc = False
        continue
    if ch == '\\':
        esc = True
        continue
    if in_str:
        if ch == in_str:
            in_str = None
        continue
    if ch in ('"', "'", '`'):
        in_str = ch
        continue
    if ch in ('(', '[', '{'):
        stack.append((ch, line))
    elif ch in (')', ']', '}'):
        if not stack:
            print(f"Error: unexpected {ch} at line {line}")
            break
        last, last_line = stack.pop()
        matches = {')': '(', ']': '[', '}': '{'}
        if matches[ch] != last:
            print(f"Error: mismatched {ch} at line {line} with {last} from line {last_line}")
            break
else:
    if stack:
        print("Unclosed:", stack[-10:])
    else:
        print("PERFECT: All brackets and braces match 100%!")
