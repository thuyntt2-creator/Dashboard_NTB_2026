import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

file_path = r"c:\Users\lap4all\Desktop\New folder\downloaded_user_sheet.xlsx"

# Load sheets
df_gtc_full = pd.read_excel(file_path, sheet_name='dataGTC gốc full hàng')
df_gtc_tts = pd.read_excel(file_path, sheet_name='dataGTC gốc TTS')
df_cocau = pd.read_excel(file_path, sheet_name='cocau')
df_san_luong = pd.read_excel(file_path, sheet_name='sản lượng')

# Create BC to AM mapping dictionary
# Drop duplicates and NaN values to make it clean
mapping_df = df_cocau[['BC', 'Am']].dropna().drop_duplicates()
bc_to_am = dict(zip(mapping_df['BC'], mapping_df['Am']))

# Clean dataGTC sheets: remove 'Grand Total' rows if any
df_gtc_full_clean = df_gtc_full[df_gtc_full['Chi tiết'] != 'Grand Total'].copy()
df_gtc_tts_clean = df_gtc_tts[df_gtc_tts['Chi tiết'] != 'Grand Total'].copy()

# Map BC to AM in dataGTC
df_gtc_full_clean['AM'] = df_gtc_full_clean['Chi tiết'].map(bc_to_am)
df_gtc_tts_clean['AM'] = df_gtc_tts_clean['Chi tiết'].map(bc_to_am)

# Filter 'Loại Hàng' in ['Hàng Mới Ca 1', 'Hàng Mới Ca 2']
df_gtc_full_filtered = df_gtc_full_clean[df_gtc_full_clean['Loại Hàng'].isin(['Hàng Mới Ca 1', 'Hàng Mới Ca 2'])]
df_gtc_tts_filtered = df_gtc_tts_clean[df_gtc_tts_clean['Loại Hàng'].isin(['Hàng Mới Ca 1', 'Hàng Mới Ca 2'])]

# Calculate Volume sums
# Pivot table for full
pivot_full = df_gtc_full_filtered.pivot_table(
    index='AM', 
    columns='Time', 
    values='Volume', 
    aggfunc='sum'
).fillna(0)

# Pivot table for tts
pivot_tts = df_gtc_tts_filtered.pivot_table(
    index='AM', 
    columns='Time', 
    values='Volume', 
    aggfunc='sum'
).fillna(0)

# Write results
output_lines = []
output_lines.append("=== CALCULATED VOLUMES (EXCLUDING HÀNG TỒN) ===")
output_lines.append("\n--- VOLUME TỔNG ---")
output_lines.append(pivot_full.to_string())
output_lines.append("\n--- VOLUME TTS ---")
output_lines.append(pivot_tts.to_string())

# Check how they differ from the 'sản lượng' sheet in the workbook
output_lines.append("\n=== COMPARING WITH 'sản lượng' SHEET ===")
output_lines.append("First 10 rows of 'sản lượng' sheet:")
output_lines.append(df_san_luong.head(10).to_string())

with open(r"c:\Users\lap4all\Desktop\New folder\calculate_wtd_vols_res.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(output_lines))

print("Results written to calculate_wtd_vols_res.txt")
