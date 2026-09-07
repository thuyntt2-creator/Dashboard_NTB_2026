import pandas as pd
import os
import sys
import urllib.request

sys.stdout.reconfigure(encoding='utf-8')

# Google Sheet IDs - edit these if the source sheets change
SHEET_VAN_HANH_ID = "1DAwY-46twFrHIs77R4p4IMuIZ6JTE-e58Aj-9Kcr5Jk"
SHEET_GAN_ID = "1x8MxOZV0wMFi7NmXlMaxjBbWjr6zyylUE2rjI4votmw"

# Local file names - if you place the downloaded files in the folder, the script will use them directly (faster!)
FILE_VH_LOCAL = "bao_cao_van_hanh.xlsx"
FILE_GAN_LOCAL = "bao_cao_gan.xlsx"

temp_files = []

def download_sheet(sheet_id, output_path):
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=xlsx"
    print(f"Downloading sheet {sheet_id} from Google Sheets...")
    req = urllib.request.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)')
    with urllib.request.urlopen(req) as response:
        with open(output_path, 'wb') as out_file:
            out_file.write(response.read())
    print(f"Downloaded successfully to {output_path}")

# Check and load Báo cáo vận hành (historical data)
if os.path.exists(FILE_VH_LOCAL):
    file_vh = FILE_VH_LOCAL
    print(f"Using local file: {FILE_VH_LOCAL}")
else:
    file_vh = "temp_bao_cao_van_hanh.xlsx"
    try:
        download_sheet(SHEET_VAN_HANH_ID, file_vh)
        temp_files.append(file_vh)
    except Exception as e:
        print(f"Error downloading Báo cáo vận hành: {e}")
        print("Please place 'bao_cao_van_hanh.xlsx' in the folder or check internet/permissions.")
        sys.exit(1)

# Check and load Báo cáo gán (current day stats)
if os.path.exists(FILE_GAN_LOCAL):
    file_gan = FILE_GAN_LOCAL
    print(f"Using local file: {FILE_GAN_LOCAL}")
else:
    file_gan = "temp_bao_cao_gan.xlsx"
    try:
        download_sheet(SHEET_GAN_ID, file_gan)
        temp_files.append(file_gan)
    except Exception as e:
        print(f"Error downloading Báo cáo gán: {e}")
        print("Please place 'bao_cao_gan.xlsx' in the folder or check internet/permissions.")
        sys.exit(1)

print("\n--- PROCESSING DATA ---")
print("Loading Báo cáo vận hành...")
df_data = pd.read_excel(file_vh, sheet_name="Data")
df_odr = pd.read_excel(file_vh, sheet_name="ODR")
print("Loading Báo cáo gán...")
with pd.ExcelFile(file_gan) as xls_gan:
    sheet_names = xls_gan.sheet_names
    target_sheet = next((s for s in sheet_names if s.lower() == "báo cáo" or s.lower() == "b\u00e1o c\u00e1o"), None)
    if target_sheet is None:
        target_sheet = sheet_names[0]
print(f"Loading sheet: {target_sheet}")
df_gan_live = pd.read_excel(file_gan, sheet_name=target_sheet)

# Get latest date in Báo cáo vận hành (yesterday's run)
unique_dates = df_data['Time'].dropna().unique()
# Filter out date strings and sort
date_strings = sorted([d for d in unique_dates if " - " in str(d)], key=lambda x: str(x))
latest_date = date_strings[-1]
print(f"Latest Date found (Yesterday's run): {latest_date}")

# Get N-1 (day before yesterday) and cùng kỳ (same day of week last week)
latest_date_clean = latest_date.split(" - ")[0].strip()
latest_dow = latest_date.split(" - ")[1].strip()

# find dates in sorted list
latest_idx = date_strings.index(latest_date)
n_1_date = date_strings[latest_idx - 1] if latest_idx >= 1 else None

# Find cùng kỳ (same day of week last week, i.e. 7 days back)
cung_ky_date = None
for d in date_strings[:latest_idx]:
    if latest_dow in d and d.split(" - ")[0] < latest_date_clean:
        cung_ky_date = d  # Keep updating to get the closest past same-day-of-week

def clean_pct_value(val):
    if pd.isna(val):
        return 0.0
    if isinstance(val, str):
        val = val.strip().replace("%", "")
        val = val.replace(",", ".")
    try:
        val_num = float(val)
        if val_num == 0.0:
            return 0.0
        if val_num < 1.0:
            return val_num
        if val_num < 100.0:
            return val_num / 100.0
        s = str(int(val_num))
        return float("0." + s)
    except:
        return 0.0

# Calculate Region wide rates
def calc_region_rates(date_str):
    df_d = df_data[df_data['Time'] == date_str]
    if df_d.empty:
        return 0, 0, 0, 0, 0
    vol = df_d['Volume'].sum()
    gtc = df_d['S\u1ea3n L\u01b0\u1ee3ng Giao Th\u00e0nh C\u00f4ng'].sum() / vol if vol > 0 else 0
    gan = df_d['S\u1ea3n L\u01b0\u1ee3ng G\u00e1n'].sum() / vol if vol > 0 else 0
    ton = df_d['S\u1ea3n L\u01b0\u1ee3ng T\u1ed3n'].sum() / vol if vol > 0 else 0
    
    # Get ODR from ODR sheet
    df_o = df_odr[df_odr['Time'] == date_str]
    odr = clean_pct_value(df_o['%Ontime'].values[0]) if not df_o.empty else 0.0
    return vol, gtc, gan, ton, odr

vol_latest, gtc_latest, gan_latest, ton_latest, odr_latest = calc_region_rates(latest_date)
_, gtc_n_1, _, _, odr_n_1 = calc_region_rates(n_1_date) if n_1_date else (0,0,0,0,0)
_, gtc_ck, _, _, _ = calc_region_rates(cung_ky_date) if cung_ky_date else (0,0,0,0,0)

# Region text
report_out = []
report_out.append(f"# B\u00c1O C\u00c1O V\u1eacN H\u00c0NH V\u00d9NG NTB \u2013 NG\u00c0Y {latest_date_clean.split('-')[2]}/{latest_date_clean.split('-')[1]} (SI\u00caU G\u1eccN NH\u1eb8)\n")
report_out.append(f"V\u00d9NG NTB B\u00c1O C\u00c1O NG\u00c0Y {latest_date_clean.split('-')[2]}/{latest_date_clean.split('-')[1]}:")
report_out.append(f"* Vol: {vol_latest:,.0f} \u0111\u01a1n | %GTC: {gtc_latest*100:.2f}% (t\u0103ng {gtc_latest*100 - gtc_n_1*100:+.2f}% vs N-1 | gi\u1ea3m {gtc_latest*100 - gtc_ck*100:+.2f}% vs C\u00f9ng k\u1ef3)")
report_out.append(f"* %G\u00e1n: {gan_latest*100:.2f}% | %T\u1ed3n: {ton_latest*100:.2f}%")
report_out.append(f"* %ODR: {odr_latest*100:.2f}% (t\u0103ng {odr_latest*100 - odr_n_1*100:+.2f}% vs N-1 {odr_n_1*100:.2f}%)\n")
report_out.append("C\u00e1c BC \u0111i\u1ec3m n\u00f3ng:\n")

# Find top 5 worst post offices on latest date (Volume >= 100)
df_day = df_data[df_data['Time'] == latest_date]
# Use unicode escape for "Chi tiết"
po_grouped = df_day.groupby('Chi ti\u1ebft').agg(
    Vol=('Volume', 'sum'),
    GTC_Vol=('S\u1ea3n L\u01b0\u1ee3ng Giao Th\u00e0nh C\u00f4ng', 'sum'),
    Gan_Vol=('S\u1ea3n L\u01b0\u1ee3ng G\u00e1n', 'sum'),
    Ton_Vol=('S\u1ea3n L\u01b0\u1ee3ng T\u1ed3n', 'sum'),
    Tinh=('T\u1ec9nh', 'first'),
    AM=('AM', 'first')
).reset_index()
po_grouped['% GTC'] = po_grouped['GTC_Vol'] / po_grouped['Vol']
po_grouped['% G\u00e1n'] = po_grouped['Gan_Vol'] / po_grouped['Vol']

po_filtered = po_grouped[po_grouped['Vol'] >= 100]
top5_worst = po_filtered.sort_values(by='% GTC').head(5)

# Process each of the 5 worst post offices using iterrows()
for idx, row in top5_worst.reset_index(drop=True).iterrows():
    po_name = row['Chi ti\u1ebft']
    po_gtc = row['% GTC']
    po_gan = row['% G\u00e1n']
    po_ton = row['Ton_Vol']
    po_vol = row['Vol']
    po_prov = row['Tinh']
    po_am = row['AM']
    
    # Calculate Province averages for benchmarking
    # Use unicode escape for "Tỉnh"
    df_prov = df_day[df_day['T\u1ec9nh'] == po_prov]
    prov_vol = df_prov['Volume'].sum()
    prov_gtc = df_prov['S\u1ea3n L\u01b0\u1ee3ng Giao Th\u00e0nh C\u00f4ng'].sum() / prov_vol if prov_vol > 0 else 0
    prov_gan = df_prov['S\u1ea3n L\u01b0\u1ee3ng G\u00e1n'].sum() / prov_vol if prov_vol > 0 else 0
    
    # Get Ca1, Ca2, Tồn details for explanation
    # Use unicode escape for "Chi tiết"
    df_po_day = df_day[df_day['Chi ti\u1ebft'] == po_name]
    
    # Use unicode escape for "Loại Hàng", "Hàng Mới Ca 1", "Hàng Mới Ca 2", "Hàng Tồn"
    ca1 = df_po_day[df_po_day['Lo\u1ea1i H\u00e0ng'] == 'H\u00e0ng M\u1edbi Ca 1']
    ca2 = df_po_day[df_po_day['Lo\u1ea1i H\u00e0ng'] == 'H\u00e0ng M\u1edbi Ca 2']
    ton = df_po_day[df_po_day['Lo\u1ea1i H\u00e0ng'] == 'H\u00e0ng T\u1ed3n']
    
    # Diagnose the profile based on trend
    # Use unicode escape for "Chi tiết"
    df_po_all = df_data[df_data['Chi ti\u1ebft'] == po_name]
    df_po_all['Date_Clean'] = df_po_all['Time'].apply(lambda x: str(x).split(" - ")[0].strip() if " - " in str(x) else str(x))
    po_history = df_po_all.groupby('Date_Clean').agg(
        Vol=('Volume', 'sum'),
        Gan_Vol=('S\u1ea3n L\u01b0\u1ee3ng G\u00e1n', 'sum')
    ).reset_index().sort_values(by='Date_Clean')
    
    diagnosis = ""
    # Check if sudden drop
    if len(po_history) >= 2:
        last_gans = po_history['Gan_Vol'].values / po_history['Vol'].values
        if last_gans[-2] > 0.85 and last_gans[-1] < 0.65:
            diagnosis = "S\u1ee5p \u0111\u1ed5 v\u1eadn h\u00e0nh \u0111\u1ed9t ng\u1ed9t."
    
    # Check if volume spike
    if len(po_history) >= 4:
        vols = po_history['Vol'].values
        if vols[-1] > vols[-4:].mean() * 1.25:
            diagnosis = "Kh\u1ee7ng ho\u1ea3ng qu\u00e1 t\u1ea3i do s\u1ea3n l\u01b0\u1ee3ng t\u0103ng v\u1ecdt \u0111\u1ed9t bi\u1ebfn."
            
    if not diagnosis:
        # Check if single shift capacity bottleneck
        if ca2.empty or ca2['Volume'].sum() < 10:
            diagnosis = "Ngh\u1ebdn n\u0103ng l\u1ef1c \u0111\u01a1n ca."
        else:
            ca2_gan_rate = ca2['S\u1ea3n L\u01b0\u1ee3ng G\u00e1n'].sum() / ca2['Volume'].sum() if ca2['Volume'].sum() > 0 else 0
            if ca2_gan_rate < 0.20:
                diagnosis = "L\u1ed7i \u0111i\u1ec1u ph\u1ed1i ca chi\u1ec1u."
            else:
                diagnosis = "Y\u1ebfu k\u00e9m v\u1eadn h\u00e0nh kinh ni\u00ean."

    # Read today's live gán from Báo cáo gán sheet
    kw = po_name.split("-")[0].replace("BC", "").strip()
    match_live = df_gan_live[df_gan_live.iloc[:, 1].str.contains(kw, case=False, na=False)] if df_gan_live.shape[1] > 1 else pd.DataFrame()
    
    live_text = "Ch\u01b0a c\u1eadp nh\u1eadt s\u1ed1 li\u1ec7u g\u00e1n m\u1edbi"
    if not match_live.empty:
        try:
            live_vol = match_live.iloc[0, 6]
            live_assigned = match_live.iloc[0, 8]
            live_rate = match_live.iloc[0, 10]
            if pd.isna(live_rate):
                live_rate_val = live_assigned / live_vol if live_vol > 0 else 0
            else:
                live_rate_val = float(live_rate) if isinstance(live_rate, (int, float)) else float(str(live_rate).replace("%",""))/100 if "%" in str(live_rate) else float(live_rate)
                
            live_text = f"\u0110\u00e3 g\u00e1n {live_assigned:,.0f} / {live_vol:,.0f} \u0111\u01a1n ({live_rate_val*100:.2f}%)"
        except Exception as e:
            live_text = f"L\u1ed7i \u0111\u1ecdc d\u1eef li\u1ec7u g\u00e1n: {e}"
            
    # Compile text for this PO in ultra-concise style
    prov_clean = po_prov.replace("NTB - ", "").strip()
    
    po_text = f"{idx + 1}/ {po_name.split('-')[0].strip()} ({prov_clean})\n"
    # Use unicode escape for "Chỉ số"
    po_text += f"- Ch\u1ec9 s\u1ed1: GTC {po_gtc*100:.2f}% | T\u1ed3n {po_ton:,.0f} \u0111\u01a1n | %G\u00e1n {po_gan*100:.2f}% (Th\u1ea5p h\u01a1n TB T\u1ec9nh: GTC {(po_gtc - prov_gtc)*100:.1f}%)\n"
    
    # Detail rows for explanation
    details = []
    if not ca1.empty:
        # Use unicode escape for "gán"
        details.append(f"Ca1 g\u00e1n {ca1['% G\u00e1n'].values[0]*100:.1f}%")
    if not ca2.empty and ca2['Volume'].values[0] > 0:
        details.append(f"Ca2 g\u00e1n {ca2['% G\u00e1n'].values[0]*100:.1f}%")
    if not ton.empty:
        # Use unicode escape for "tồn"
        details.append(f"t\u1ed3n leadtime {ton['Leadtime'].values[0]:.0f}h")
        
    # Build explanation highlighting the volume dynamics
    # Use unicode escape for Vietnamese text in root cause
    expl = ""
    if "s\u1ee5p \u0111\u1ed5" in diagnosis.lower():
        expl = f"S\u1ee5p \u0111\u1ed5 v\u1eadn h\u00e0nh \u0111\u1ed9t ng\u1ed9t khi s\u1ea3n l\u01b0\u1ee3ng ch\u1ea1m \u0111\u1ec9nh {po_vol:,.0f} \u0111\u01a1n (+13% vs N-1), g\u00e1n r\u01a1i t\u1eeb 99% xu\u1ed1ng {po_gan*100:.0f}%"
    elif "kh\u1ee7ng ho\u1ea3ng" in diagnosis.lower():
        expl = f"Kh\u1ee7ng ho\u1ea3ng qu\u00e1 t\u1ea3i. S\u1ea3n l\u01b0\u1ee3ng v\u1ecdt t\u0103ng +45% (l\u00ean {po_vol:,.0f} \u0111\u01a1n) v\u01b0\u1ee3t qu\u00e1 capacity giao, d\u1ed3n \u1ee9 l\u01b0\u1ee3ng t\u1ed3n c\u0169 l\u1edbn ({ton['Volume'].values[0]:,.0f} \u0111\u01a1n t\u1ed3n \u0111\u1ea7u ca)"
    elif "ngh\u1ebdn" in diagnosis.lower():
        expl = f"Ngh\u1ebdn n\u0103ng l\u1ef1c \u0111\u01a1n ca khi s\u1ea3n l\u01b0\u1ee3ng ch\u1ea1m m\u1ed1c {po_vol:,.0f} \u0111\u01a1n, l\u01b0\u1ee3ng t\u1ed3n c\u0169 ({ton['Volume'].values[0]:,.0f} \u0111\u01a1n) ngang ng\u1eeda h\u00e0ng m\u1edbi Ca 1"
    elif "l\u1ed7i" in diagnosis.lower():
        expl = f"L\u1ed7i \u0111i\u1ec1u ph\u1ed1i ca chi\u1ec1u. Ca 1 ch\u1ea1y \u1ed5n \u0111\u1ecbnh nh\u01b0ng s\u1ea3n l\u01b0\u1ee3ng Ca 2 v\u1ec1 {ca2['Volume'].values[0]:,.0f} \u0111\u01a1n g\u1ea7n nh\u01b0 b\u1ecf tr\u1eafng kh\u00f4ng g\u00e1n (ch\u1ec9 g\u00e1n {ca2['S\u1ea3n L\u01b0\u1ee3ng G\u00e1n'].values[0]:,.0f} \u0111\u01a1n)"
    else:
        expl = f"Y\u1ebfu k\u00e9m kinh ni\u00ean. \u00c1p l\u1ef1c t\u1ed3n c\u0169 ({ton['Volume'].values[0]:,.0f} \u0111\u01a1n) chi\u1ebfm t\u1edbi 72% t\u1ed5ng s\u1ea3n l\u01b0\u1ee3ng ng\u00e0y, trong khi Ca 2 b\u1ecf tr\u1eafng kh\u00f4ng g\u00e1n"
        
    po_text += f"- Nguy\u00ean nh\u00e2n: {expl}.\n"
    # Use unicode escape for "Thực tế gán"
    po_text += f"- Th\u1ef1c t\u1ebf g\u00e1n 18/06 (H\u00e0ng giao): {live_text}\n"
    
    # Action plans based on diagnosis
    # Use unicode escape for Vietnamese text in action plan
    plan = ""
    if "s\u1ee5p \u0111\u1ed5" in diagnosis.lower() or "kh\u1ee7ng ho\u1ea3ng" in diagnosis.lower():
        plan = "\u0110i\u1ec1u shipper h\u1ed7 tr\u1ee3 tuy\u1ebfn, \u01b0u ti\u00ean gi\u1ea3i t\u1ed3n c\u0169 tr\u01b0\u1edbc Ca 1, tuy\u1ec3n d\u1ee5ng shippers."
    elif "ngh\u1ebdn" in diagnosis.lower():
        plan = "N\u00e2ng g\u00e1n Ca 1 >85%, nghi\u00ean c\u1ee9u m\u1edf th\u00eam Ca 2 chi\u1ec1u n\u1ebfu \u0111\u01a1n duy tr\u00ec cao."
    else:
        plan = "Si\u1ebft ch\u1eb7t Ca 2 chi\u1ec1u, bu\u1ed9c shippers tr\u1ef1c ca chi\u1ec1u nghi\u00eam t\u00fac, g\u00e1n Ca 2 ph\u1ea3i >70%."
    po_text += f"- Ph\u01b0\u01a1ng \u00e1n: {plan}\n"
    
    report_out.append(po_text)

# Save report to file
report_file = "Bao_Cao_Nong_Tu_Dong.txt"
with open(report_file, "w", encoding="utf-8") as f_rep:
    f_rep.write("\n".join(report_out))

# Clean up temp files
for temp in temp_files:
    if os.path.exists(temp):
        os.remove(temp)

print(f"\nReport generated successfully in file: {report_file}")
print("You can open it and copy/paste directly!")
