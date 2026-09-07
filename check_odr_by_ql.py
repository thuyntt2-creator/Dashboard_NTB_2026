import pandas as pd

file_path = r"c:\Users\lap4all\Desktop\New folder\downloaded_user_sheet.xlsx"
df_odr_full = pd.read_excel(file_path, sheet_name='dataODRfull hàng ')
df_odr_tts = pd.read_excel(file_path, sheet_name='dataODR TTS')

# Calculate weighted average ODR by Quản lý and Time
df_odr_full['Vol_Ontime'] = df_odr_full['GTC'] * df_odr_full['%Ontime']
df_odr_tts['Vol_Ontime'] = df_odr_tts['GTC'] * df_odr_tts['%Ontime']

grouped_full = df_odr_full.groupby(['Quản lý', 'Time']).agg(
    Total_Vol=('GTC', 'sum'),
    Total_Ontime=('Vol_Ontime', 'sum')
).reset_index()
grouped_full['ODR'] = grouped_full['Total_Ontime'] / grouped_full['Total_Vol']

grouped_tts = df_odr_tts.groupby(['Quản lý', 'Time']).agg(
    Total_Vol=('GTC', 'sum'),
    Total_Ontime=('Vol_Ontime', 'sum')
).reset_index()
grouped_tts['ODR'] = grouped_tts['Total_Ontime'] / grouped_tts['Total_Vol']

pivot_full = grouped_full.pivot(index='Quản lý', columns='Time', values='ODR')
pivot_tts = grouped_tts.pivot(index='Quản lý', columns='Time', values='ODR')

output = []
output.append("=== CALCULATED ODR FULL BY QUẢN LÝ ===")
output.append(pivot_full.to_string())
output.append("\n=== CALCULATED ODR TTS BY QUẢN LÝ ===")
output.append(pivot_tts.to_string())

# Check simple average of %Ontime in dataODR TTS by Quản lý
grouped_tts_simple = df_odr_tts.groupby(['Quản lý', 'Time'])['%Ontime'].mean().reset_index()
pivot_tts_simple = grouped_tts_simple.pivot(index='Quản lý', columns='Time', values='%Ontime')
output.append("\n=== SIMPLE AVERAGE ODR TTS BY QUẢN LÝ ===")
output.append(pivot_tts_simple.to_string())

with open(r"c:\Users\lap4all\Desktop\New folder\check_odr_by_ql_res.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(output))

print("Results written.")
