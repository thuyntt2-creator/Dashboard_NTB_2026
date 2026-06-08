import openpyxl
import os

workspace_dir = r"c:\Users\lap4all\Desktop\New folder"
output_path = os.path.join(workspace_dir, "inspect_all_workbooks.txt")

with open(output_path, "w", encoding="utf-8") as f:
    for filename in os.listdir(workspace_dir):
        if filename.endswith(".xlsx"):
            file_path = os.path.join(workspace_dir, filename)
            f.write(f"\n=========================================\n")
            f.write(f"File: {filename}\n")
            f.write(f"=========================================\n")
            try:
                wb = openpyxl.load_workbook(file_path, read_only=True)
                f.write(f"Sheets: {wb.sheetnames}\n")
            except Exception as e:
                f.write(f"Error: {e}\n")

print("Done listing sheets of all workbooks.")
