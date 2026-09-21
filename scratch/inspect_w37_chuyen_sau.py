import docx

doc = docx.Document('KICH_BAN_THUYET_TRINH_W37_INSIGHT_CHUYEN_SAU.docx')
print(f"Total paragraphs: {len(doc.paragraphs)}")
print(f"Total tables: {len(doc.tables)}")

print("\n--- ALL PARAGRAPHS ---")
for i, p in enumerate(doc.paragraphs):
    if p.text.strip():
        print(f"P{i+1} [{p.style.name}]: {p.text}")

print("\n--- ALL TABLES ---")
for t_idx, tbl in enumerate(doc.tables):
    print(f"\n=== TABLE {t_idx+1}: {len(tbl.rows)} rows x {len(tbl.columns)} cols ===")
    for r_idx, row in enumerate(tbl.rows):
        cells = [c.text.replace('\n', ' ').strip() for c in row.cells]
        # remove duplicate merged cells representation
        print(f"  R{r_idx+1}: " + " | ".join(cells[:8]))
