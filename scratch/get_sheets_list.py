import urllib.request
import openpyxl

sheet_id = "1U-vA09JQWwC6huGi95cJ19pDdrxOt_qiMjwAxM6AvbY"
xlsx_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=xlsx"

print("Downloading XLSX...")
req = urllib.request.Request(xlsx_url)
req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)')

try:
    with urllib.request.urlopen(req) as response:
        xlsx_data = response.read()
    print("XLSX downloaded successfully! Size:", len(xlsx_data))
    
    # Save the file
    output_path = "scratch/downloaded_sheets.xlsx"
    with open(output_path, "wb") as f:
        f.write(xlsx_data)
    print("Saved XLSX to", output_path)
    
    # Open with openpyxl to get sheet names
    wb = openpyxl.load_workbook(output_path, read_only=True)
    print("\nSheet names in workbook:")
    for name in wb.sheetnames:
        print("  -", name)
        
except Exception as e:
    import traceback
    traceback.print_exc()
