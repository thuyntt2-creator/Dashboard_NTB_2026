import docx, sys
sys.stdout.reconfigure(encoding='utf-8')

file_path = r"C:\Users\lap4all\Downloads\KICH_BAN_THUYET_TRINH_W39_NAM_TRUNG_BO (16).docx"
doc = docx.Document(file_path)

def print_table_first_part(idx):
    if idx >= len(doc.tables):
        return
    tbl = doc.tables[idx]
    print(f"\n==================== TABLE {idx+1} (FIRST 800 CHARS) ====================")
    for r in tbl.rows:
        for c in r.cells:
            print(c.text.strip()[:800])

print_table_first_part(0) # Table 1 (Tổng quan)
print_table_first_part(1) # Table 2 (Sản lượng)
print_table_first_part(2) # Table 3 (GTC Tổng)
print_table_first_part(3) # Table 4 (GTC Ca 1 TTS)
