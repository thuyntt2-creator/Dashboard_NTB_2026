import openpyxl
import os

file_path = r"c:\Users\lap4all\Desktop\New folder\downloaded_user_sheet.xlsx"
wb = openpyxl.load_workbook(file_path, data_only=False)

output = []
for name in wb.sheetnames:
    ws = wb[name]
    output.append(f"\n=========================================\nSHEET: {name}\n=========================================")
    # Let's read the first 10 rows and 10 columns
    for row in range(1, 15):
        row_vals = []
        for col in range(1, 15):
            cell = ws.cell(row=row, column=col)
            val = cell.value
            if val is not None:
                row_vals.append(f"Col {col}: {val}")
        if row_vals:
            output.append(f"Row {row}: " + " | ".join(row_vals))

with open(r"c:\Users\lap4all\Desktop\New folder\user_formulas_info.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(output))

print("Formulas written to user_formulas_info.txt")
