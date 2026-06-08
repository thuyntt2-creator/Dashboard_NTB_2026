import os

def main():
    file_path = r"C:\Users\lap4all\Desktop\New folder\templates\index.html"
    with open(file_path, 'r', encoding='utf-8') as f:
        html = f.read()
        
    lines = html.split('\n')
    js_lines = lines[2960:6181]
    
    in_string = None
    string_start_line = 0
    string_start_col = 0
    escape = False
    
    for i, line in enumerate(js_lines):
        line_num = 2961 + i
        for col, char in enumerate(line):
            if escape:
                escape = False
                continue
            if in_string:
                if char == '\\':
                    escape = True
                elif char == in_string:
                    print(f"Closed string {in_string} at line {line_num}, col {col+1} (opened at {string_start_line}:{string_start_col})")
                    in_string = None
                continue
                
            if char in ["'", '"', '`']:
                in_string = char
                string_start_line = line_num
                string_start_col = col + 1
                print(f"Opened string {char} at line {line_num}, col {col+1}")

if __name__ == "__main__":
    main()
