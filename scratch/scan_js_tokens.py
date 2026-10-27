with open('app.js', 'r', encoding='utf-8') as f:
    text = f.read()

# Let's track curly braces and parens ignoring strings and comments
in_str = None
in_comment = False
in_block_comment = False
escape = False

brace_stack = []
paren_stack = []

line_no = 1
col_no = 1

errors = []

i = 0
n = len(text)
while i < n:
    ch = text[i]
    if ch == '\n':
        line_no += 1
        col_no = 1
        i += 1
        if in_comment:
            in_comment = False
        continue
    
    if in_comment:
        i += 1
        col_no += 1
        continue
        
    if in_block_comment:
        if ch == '*' and i + 1 < n and text[i+1] == '/':
            in_block_comment = False
            i += 2
            col_no += 2
            continue
        i += 1
        col_no += 1
        continue
        
    if in_str:
        if escape:
            escape = False
        elif ch == '\\':
            escape = True
        elif ch == in_str:
            in_str = None
        i += 1
        col_no += 1
        continue
        
    # Check start of string or comment
    if ch == '/' and i + 1 < n and text[i+1] == '/':
        in_comment = True
        i += 2
        col_no += 2
        continue
    if ch == '/' and i + 1 < n and text[i+1] == '*':
        in_block_comment = True
        i += 2
        col_no += 2
        continue
    if ch in ("'", '"', '`'):
        in_str = ch
        i += 1
        col_no += 1
        continue
        
    if ch == '{':
        brace_stack.append((line_no, col_no))
    elif ch == '}':
        if brace_stack:
            brace_stack.pop()
        else:
            errors.append(f"Unexpected '}}' at line {line_no}:{col_no}")
            
    elif ch == '(':
        paren_stack.append((line_no, col_no))
    elif ch == ')':
        if paren_stack:
            paren_stack.pop()
        else:
            errors.append(f"Unexpected ')' at line {line_no}:{col_no}")

    i += 1
    col_no += 1

print(f"Finished parsing. Errors: {len(errors)}")
for e in errors[:10]:
    print(" ", e)

print(f"Unclosed braces count: {len(brace_stack)}")
if brace_stack:
    for b in brace_stack[-5:]:
        print(f"  Unclosed '{{' opened at line {b[0]}:{b[1]}")

print(f"Unclosed parens count: {len(paren_stack)}")
if paren_stack:
    for p in paren_stack[-5:]:
        print(f"  Unclosed '(' opened at line {p[0]}:{p[1]}")
