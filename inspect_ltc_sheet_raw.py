import openpyxl

file_path = r"c:\Users\lap4all\Desktop\New folder\downloaded_user_sheet.xlsx"
wb = openpyxl.load_workbook(file_path, data_only=False)
ws = wb['LTC']

output = []
for row in range(1, 15):
    row_vals = []
    for col in range(1, 15):
        cell = ws.cell(row=row, column=col)
        val = cell.value
        if val is not None:
            row_vals.append(f"Col {col}: {val}")
    if row_vals:
        output.append(f"Row {row}: " + " | ".join(row_vals))

with open(r"c:\Users\lap4all\Desktop\New folder\ltc_formulas_res.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(output))

print("Formulas written to ltc_formulas_res.txt")
