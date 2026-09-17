# -*- coding: utf-8 -*-

def main():
    with open('scratch/test_compact.py', 'r', encoding='utf-8') as f:
        text = f.read()
    
    parts = text.split('"""')
    report = parts[1].strip()
    print("Initial length:", len(report))

if __name__ == '__main__':
    main()
