import re
import os

def check_js(js_code, start_line):
    lines = js_code.split('\n')
    stack = []
    in_string = None  # None, or "'", '"', '`'
    string_start_line = 0
    string_start_col = 0
    in_line_comment = False
    in_block_comment = False
    escape = False
    
    for r_idx, line in enumerate(lines):
        line_num = start_line + r_idx
        c_idx = 0
        while c_idx < len(line):
            char = line[c_idx]
            
            if escape:
                escape = False
                c_idx += 1
                continue
                
            if in_line_comment:
                break
                
            if in_block_comment:
                if char == '*' and c_idx + 1 < len(line) and line[c_idx+1] == '/':
                    in_block_comment = False
                    c_idx += 2
                else:
                    c_idx += 1
                continue
                
            if in_string:
                if char == '\\':
                    escape = True
                elif char == in_string:
                    in_string = None
                c_idx += 1
                continue
                
            # Check for comment start
            if char == '/' and c_idx + 1 < len(line):
                next_char = line[c_idx+1]
                if next_char == '/':
                    in_line_comment = True
                    c_idx += 2
                    continue
                elif next_char == '*':
                    in_block_comment = True
                    c_idx += 2
                    continue
                else:
                    # Could be regex literal or division
                    # Scan forward on the same line to find the closing '/'
                    # If we find it, we can skip the regex content
                    found_closing = -1
                    scan_idx = c_idx + 1
                    scan_escape = False
                    while scan_idx < len(line):
                        scan_char = line[scan_idx]
                        if scan_escape:
                            scan_escape = False
                            scan_idx += 1
                            continue
                        if scan_char == '\\':
                            scan_escape = True
                            scan_idx += 1
                            continue
                        if scan_char == '/':
                            found_closing = scan_idx
                            break
                        scan_idx += 1
                    
                    if found_closing != -1:
                        # Skip the regex/division block
                        c_idx = found_closing + 1
                        # Skip flags if any
                        while c_idx < len(line) and line[c_idx] in ['g', 'i', 'm', 'y', 'u', 's']:
                            c_idx += 1
                        continue
                    
            # Check for string start
            if char in ["'", '"', '`']:
                in_string = char
                string_start_line = line_num
                string_start_col = c_idx + 1
                c_idx += 1
                continue
                
            # Brackets check
            if char in ['{', '(', '[']:
                stack.append((char, line_num, c_idx + 1))
            elif char in ['}', ')', ']']:
                if not stack:
                    print(f"Unmatched closing bracket '{char}' at line {line_num}, col {c_idx+1}")
                    return False
                top, top_l, top_c = stack.pop()
                pairs = {'}': '{', ')': '(', ']': '['}
                if pairs[char] != top:
                    print(f"Mismatch: '{char}' at line {line_num}, col {c_idx+1} does not match '{top}' from line {top_l}, col {top_c}")
                    return False
            
            c_idx += 1
        in_line_comment = False
        
    if in_string:
        print(f"Unclosed string of type {in_string} opened at line {string_start_line}, col {string_start_col}")
        return False
    if in_block_comment:
        print(f"Unclosed block comment /* at end of script")
        return False
    if stack:
        print(f"Unclosed opening brackets at end of script:")
        for item in stack:
            print(f"  '{item[0]}' at line {item[1]}, col {item[2]}")
        return False
        
    print("No unbalanced brackets found in this block!")
    return True

def main():
    file_path = r"C:\Users\lap4all\Desktop\New folder\templates\index.html"
    with open(file_path, 'r', encoding='utf-8') as f:
        html = f.read()
        
    lines = html.split('\n')
    in_script = False
    script_lines = []
    script_start = 0
    
    for idx, line in enumerate(lines):
        line_num = idx + 1
        if "<script>" in line and not in_script:
            in_script = True
            script_start = line_num
            script_lines = []
        elif "</script>" in line and in_script:
            in_script = False
            js_code = '\n'.join(script_lines)
            print(f"\n--- Checking script block starting at line {script_start} ---")
            check_js(js_code, script_start + 1)
        elif in_script:
            script_lines.append(line)

if __name__ == "__main__":
    main()
