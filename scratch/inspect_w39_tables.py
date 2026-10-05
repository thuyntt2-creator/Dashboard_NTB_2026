import docx, sys
sys.stdout.reconfigure(encoding='utf-8')

file_path = r"C:\Users\lap4all\Downloads\KICH_BAN_THUYET_TRINH_W39_NAM_TRUNG_BO (16).docx"
doc = docx.Document(file_path)

print(f"Tables count: {len(doc.tables)}")

for idx, tbl in enumerate(doc.tables):
    print(f"\n==================== TABLE {idx+1} (Rows: {len(tbl.rows)}, Cols: {len(tbl.columns)}) ====================")
    for r_idx, row in enumerate(tbl.rows):
        for c_idx, cell in enumerate(row.cells):
            cell_text = cell.text.strip()
            # print first 500 chars of cell
            first_line = cell_text.split('\n')[0] if cell_text else ""
            print(f"  [R{r_idx}C{c_idx}] (len={len(cell_text)}): {first_line[:100]}")
            # print up to 5 paragraphs inside cell
            paras = [p.text for p in cell.paragraphs if p.text.strip()]
            for p_i, p_txt in enumerate(paras[:8]):
                print(f"      p{p_i}: {p_txt[:120]}")
        if r_idx >= 3:
            print("  ... (more rows truncated)")
            break
