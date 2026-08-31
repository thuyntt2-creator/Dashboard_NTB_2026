import pickle
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r"c:\Users\lap4all\Desktop\New folder\scratch\raw_sheets_data.pkl", "rb") as f:
    data = pickle.load(f)

with open(r"c:\Users\lap4all\Desktop\New folder\scratch\user_sheets_preview.txt", "w", encoding="utf-8") as f:
    for s_name in ['RPT_Ngày', 'RPT_Tuần', 'RPT_Tháng', 'RPT_KHM']:
        f.write(f"\n==================== SHEET: {s_name} ====================\n")
        df = data[s_name]
        # write all rows and columns
        f.write(df.to_string())
        f.write("\n")
print("Saved all reports to user_sheets_preview.txt")
