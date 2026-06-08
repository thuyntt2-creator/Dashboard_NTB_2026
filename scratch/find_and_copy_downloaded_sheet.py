import os
import shutil
import glob
import pandas as pd

downloads_dir = r"C:\Users\lap4all\Downloads"
workspace_dir = r"c:\Users\lap4all\Desktop\New folder"
dest_path = os.path.join(workspace_dir, "vols_tao_don.xlsx")

# Search for recently modified xlsx files in Downloads
files = glob.glob(os.path.join(downloads_dir, "*.xlsx"))
if not files:
    print("No xlsx files found in Downloads folder.")
else:
    # Sort files by modification time
    files.sort(key=os.path.getmtime, reverse=True)
    
    print("Recent XLSX files in Downloads:")
    recent_files = []
    for f in files[:5]:
        basename = os.path.basename(f)
        # safe print with replacement for console
        safe_name = basename.encode('ascii', errors='replace').decode('ascii')
        print(f"  {safe_name} - Modified: {os.path.getmtime(f)}")
        
    # Let's find the one matching "NTB" or most recent
    target_file = files[0]
    safe_target_name = os.path.basename(target_file).encode('ascii', errors='replace').decode('ascii')
    print(f"\nSelecting most recent file: {safe_target_name}")
    
    # Copy it
    shutil.copy2(target_file, dest_path)
    print(f"Copied successfully to {dest_path}")
    
    # Verify sheet names
    try:
        xls = pd.ExcelFile(dest_path)
        print(f"Sheet names in copied file: {xls.sheet_names}")
        for s in xls.sheet_names:
            df = pd.read_excel(xls, sheet_name=s, nrows=3)
            print(f"\nSheet '{s}' Columns:")
            print(list(df.columns))
            print("Preview:")
            print(df.to_string())
    except Exception as e:
        print(f"Error inspecting sheet: {e}")
