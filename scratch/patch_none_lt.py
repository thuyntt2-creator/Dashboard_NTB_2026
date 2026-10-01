import os

file_path = r'C:\Users\lap4all\Documents\Auto report\none LT KTC.py'
with open(file_path, 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Update write_analysis_to_gsheet to safely check columns
old_func_start = """def write_analysis_to_gsheet(sh, df):
    def agg(group_cols):"""

new_func_start = """def write_analysis_to_gsheet(sh, df):
    if df is None or df.empty or 'loai_kho' not in df.columns or 'ten_kho' not in df.columns:
        print("⚠️ Tab 'raw' không có cột 'loai_kho' / 'ten_kho' của Leadtime KTC. Bỏ qua ghi sheet phân tích.")
        return None, None

    def agg(group_cols):"""

assert old_func_start in code, "Old func start not found"
code = code.replace(old_func_start, new_func_start, 1)

# 2. Update main call
old_main_call = """    print(f"📝 Ghi bảng phân tích (ngày {REPORT_DATE}) vào Google Sheet...")
    write_analysis_to_gsheet(sh_lt, df_lt)"""

new_main_call = """    if df_lt is not None and not df_lt.empty and 'loai_kho' in df_lt.columns:
        print(f"📝 Ghi bảng phân tích (ngày {REPORT_DATE}) vào Google Sheet...")
        write_analysis_to_gsheet(sh_lt, df_lt)
    else:
        print(f"ℹ️ [Chế độ None LT] Bỏ qua ghi bảng phân tích Leadtime (tab 'raw' không chứa data Leadtime).")"""

assert old_main_call in code, "Old main call not found"
code = code.replace(old_main_call, new_main_call, 1)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(code)

print("Successfully updated none LT KTC.py!")
