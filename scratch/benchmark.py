import os
import sys
import time
import pandas as pd

sys.stdout.reconfigure(encoding='utf-8')

WORKSPACE_DIR = r"c:\Users\lap4all\Desktop\New folder"

files = [
    ('Aging _5 ngày.xlsx', ["Đơn giao aging trên 5 ngày", "Cơ cấu"]),
    ('Copy o NTB - BÁO CÁO VẬN HÀNH.xlsx', ["Datagtc", "Dataltc", "Cơ cấu"]),
    ('OPR TTS.xlsx', ["OPR", "OE_madh", "rawopr"]),
    ('Treo luân chuyển GIAO_TRẢ by IMTHIR.xlsx', ["stuck", "Cơ cấu"]),
    ('buu_cuc_bat_on.xlsx', None),
    ('off_tuyen_spe.xlsx', None),
    ('vols_tao_don.xlsx', None)
]

for filename, sheets in files:
    path = os.path.join(WORKSPACE_DIR, filename)
    if os.path.exists(path):
        start = time.time()
        print(f"Loading {filename}...")
        try:
            if sheets:
                with pd.ExcelFile(path) as xls:
                    for s in sheets:
                        s_lower = s.lower()
                        # Find matching sheet by case-insensitive name
                        found_sheet = None
                        for name in xls.sheet_names:
                            if name.strip().lower() == s_lower:
                                found_sheet = name
                                break
                        if found_sheet:
                            s_start = time.time()
                            df = pd.read_excel(xls, sheet_name=found_sheet)
                            print(f"  Sheet '{found_sheet}': {len(df)} rows, took {time.time() - s_start:.2f}s")
                        else:
                            print(f"  Sheet '{s}' not found in {xls.sheet_names}")
            else:
                xls = pd.ExcelFile(path)
                s = xls.sheet_names[0]
                df = pd.read_excel(xls, sheet_name=s)
                print(f"  First sheet '{s}': {len(df)} rows, took {time.time() - start:.2f}s")
        except Exception as e:
            print(f"  Error loading {filename}: {e}")
        print(f"Total for {filename}: {time.time() - start:.2f}s\n")
    else:
        print(f"File {filename} does not exist.\n")
