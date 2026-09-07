import pandas as pd
import sys

# Set encoding for print just in case
sys.stdout.reconfigure(encoding='utf-8')

file_path = r"c:\Users\lap4all\Desktop\New folder\downloaded_user_sheet.xlsx"

# Load sheets
df_gtc_full = pd.read_excel(file_path, sheet_name='dataGTC gốc full hàng')
df_gtc_tts = pd.read_excel(file_path, sheet_name='dataGTC gốc TTS')
df_cocau = pd.read_excel(file_path, sheet_name='cocau')
df_san_luong = pd.read_excel(file_path, sheet_name='sản lượng')

output_lines = []

output_lines.append(f"Unique values in dataGTC full 'Loại Hàng': {df_gtc_full['Loại Hàng'].unique().tolist()}")
output_lines.append(f"Unique values in dataGTC TTS 'Loại Hàng': {df_gtc_tts['Loại Hàng'].unique().tolist()}")

# Let's inspect cocau mapping columns
output_lines.append(f"cocau columns: {df_cocau.columns.tolist()}")

# Let's see if Chi tiết in dataGTC exists in cocau BC or Bưu cục
gtc_chi_tiet = set(df_gtc_full['Chi tiết'].unique())
cocau_bc = set(df_cocau['BC'].dropna().unique())
cocau_buucuc = set(df_cocau['Bưu cục'].dropna().unique())

output_lines.append(f"\nNumber of unique Chi tiết in dataGTC full: {len(gtc_chi_tiet)}")
output_lines.append(f"Number of unique BC in cocau: {len(cocau_bc)}")
output_lines.append(f"Number of unique Bưu cục in cocau: {len(cocau_buucuc)}")

# Check exact matches
matches_bc = gtc_chi_tiet.intersection(cocau_bc)
matches_buucuc = gtc_chi_tiet.intersection(cocau_buucuc)
output_lines.append(f"Exact matches with BC: {len(matches_bc)}")
output_lines.append(f"Exact matches with Bưu cục: {len(matches_buucuc)}")

unmatched = gtc_chi_tiet - matches_bc - matches_buucuc
output_lines.append(f"Unmatched Chi tiết: {len(unmatched)}")
if unmatched:
    output_lines.append("Some unmatched examples:")
    for x in list(unmatched)[:10]:
        output_lines.append(f"  - {x}")

# Let's write output
with open(r"c:\Users\lap4all\Desktop\New folder\test_mapping_res.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(output_lines))

print("Mapping verification written to test_mapping_res.txt")
