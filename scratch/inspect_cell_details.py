import pickle
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r"c:\Users\lap4all\Desktop\New folder\scratch\raw_sheets_data.pkl", "rb") as f:
    data = pickle.load(f)

df_rpt_ngay = data['RPT_Ngày']
print("Row 8 (Khác) details:")
row_8 = df_rpt_ngay.iloc[8]
for i, val in enumerate(row_8):
    print(f"Col {i}: {val} (type: {type(val)})")
