import pandas as pd
import os
import sys
import urllib.request
import json
import re
import unicodedata
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

def load_live_gan_data_from_raw():
    temp_ghn_path = r"c:\Users\lap4all\.gemini\antigravity-ide\scratch\temp_ghn.xlsx"
    if not os.path.exists(temp_ghn_path):
        temp_ghn_path = r"C:\Users\lap4all\Desktop\Backlog_Automation\temp_ghn.xlsx"
        if not os.path.exists(temp_ghn_path):
            temp_ghn_path = r"c:\Users\lap4all\Documents\Auto report\temp_ghn.xlsx"
            if not os.path.exists(temp_ghn_path):
                return None, None

    print(f"Calculating live gán statistics from local raw data: {temp_ghn_path}...")
    try:
        # Load local mapping file
        co_cau_path = os.path.join(script_dir, "co_cau_ntb.csv")
        if not os.path.exists(co_cau_path):
            co_cau_path = os.path.join(script_dir, "co_cau_ntb.xlsx")
            if os.path.exists(co_cau_path):
                co_df = pd.read_excel(co_cau_path)
            else:
                return None, None
        else:
            co_df = pd.read_csv(co_cau_path)
            
        co_df['warehouse_id'] = co_df['warehouse_id'].astype(str).str.strip()
        if 'Bưu cục' in co_df.columns:
            co_df['Bưu cục'] = co_df['Bưu cục'].astype(str).str.strip().apply(lambda x: unicodedata.normalize('NFC', x))
            
        raw_df = pd.read_excel(temp_ghn_path, skiprows=1).fillna("")
        raw_df['Mã bưu cục'] = raw_df['Mã bưu cục'].astype(str).str.strip()
        
        df_merged = pd.merge(raw_df, co_df, left_on='Mã bưu cục', right_on='warehouse_id', how='left')
        df_merged['Bưu cục'] = df_merged['Bưu cục'].fillna("Bưu cục " + df_merged['Mã bưu cục']).astype(str).str.strip().apply(lambda x: unicodedata.normalize('NFC', x))
        
        df_merged['is_giao'] = (df_merged['Loại đơn'] != 'Lấy') & (df_merged['Loại đơn'] != 'Trả')
        df_merged['is_da_gan'] = df_merged['Trạng thái'].isin(['Đang có chuyến đi trong ngày', 'Đã có chuyến đi trong ngày'])
        
        # Parse live date from metadata in row 0
        meta_df = pd.read_excel(temp_ghn_path, nrows=1)
        live_date = None
        if not meta_df.empty:
            meta_str = str(meta_df.columns[0])
            match = re.search(r'(\d{2})/(\d{2})', meta_str)
            if match:
                live_date = f"{match.group(1)}/{match.group(2)}"
        if not live_date:
            live_date = datetime.now().strftime("%d/%m")
            
        return df_merged, live_date
    except Exception as e:
        print(f"Error calculating live statistics from raw data: {e}")
        return None, None

# Google Sheet IDs - edit these if the source sheets change
SHEET_VAN_HANH_ID = "1DAwY-46twFrHIs77R4p4IMuIZ6JTE-e58Aj-9Kcr5Jk"
SHEET_GAN_ID = "1DuMW_ajrtrmLlMNslJY2UIMWygVY1cFD4QhKnX9YGNQ"
SHEET_NHAN_SU_URL = "https://docs.google.com/spreadsheets/d/1PjzFqJO-wkQ8SNsPHD721_CbPr6c_ArZKuGGU6KqDZg/export?format=xlsx"

# Get the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Local file names - resolved relative to the script directory
FILE_VH_LOCAL = os.path.join(script_dir, "bao_cao_van_hanh.xlsx")
FILE_GAN_LOCAL = os.path.join(script_dir, "bao_cao_gan.xlsx")

temp_files = []

def download_sheet(sheet_id, output_path):
    # Try authenticated download first if gspread and credentials are available
    try:
        import gspread
        from google.oauth2.service_account import Credentials
        
        # Load dotenv to get GOOGLE_APPLICATION_CREDENTIALS if exists
        try:
            from dotenv import load_dotenv
            env_path = r"c:\Users\lap4all\Desktop\New folder\.env"
            if os.path.exists(env_path):
                load_dotenv(dotenv_path=env_path, override=True)
            else:
                load_dotenv()
        except Exception:
            pass

        credentials_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
        candidates = [
            credentials_path,
            r"C:\Users\lap4all\Desktop\Backlog_Automation\credentials.json",
            r"C:\Users\lap4all\Downloads\credentials.json",
            r"C:\Users\lap4all\Downloads\service_account.json",
            r"C:\Users\lap4all\Desktop\credentials.json",
            os.path.join(script_dir, "credentials.json"),
            os.path.join(script_dir, "service_account.json"),
        ]
        
        creds_file = None
        for path in candidates:
            if path and os.path.isfile(path):
                creds_file = path
                break
                
        if creds_file:
            print(f"Using service account for download: {creds_file}")
            scopes = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
            creds = Credentials.from_service_account_file(creds_file, scopes=scopes)
            
            # If requesting CSV, find the "Báo Cáo" worksheet and get its gid
            if output_path.endswith(".csv"):
                gc = gspread.authorize(creds)
                sh = gc.open_by_key(sheet_id)
                worksheets = sh.worksheets()
                ws = next((w for w in worksheets if w.title.lower() == "báo cáo" or w.title.lower() == "b\u00e1o c\u00e1o"), worksheets[0])
                gid = ws.id
                url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"
            else:
                url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=xlsx"

            from google.auth.transport.requests import AuthorizedSession
            session = AuthorizedSession(creds)
            print(f"Downloading sheet {sheet_id} using authenticated session...")
            response = session.get(url, timeout=120)
            if response.status_code == 200:
                with open(output_path, 'wb') as out_file:
                    out_file.write(response.content)
                print(f"Downloaded successfully via authenticated session to {output_path}")
                return
            else:
                print(f"Authenticated download failed with code {response.status_code}, falling back to unauthenticated...")
    except Exception as e:
        print(f"Authenticated download skipped or failed: {e}. Falling back to unauthenticated...")

    # Unauthenticated fallback
    if output_path.endswith(".csv"):
        url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid=0"
    else:
        url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=xlsx"
        
    print(f"Downloading sheet {sheet_id} from Google Sheets (unauthenticated)...")
    req = urllib.request.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)')
    with urllib.request.urlopen(req, timeout=120) as response:
        with open(output_path, 'wb') as out_file:
            out_file.write(response.read())
    print(f"Downloaded successfully to {output_path}")


# Check and load Báo cáo vận hành (historical data)
if os.path.exists(FILE_VH_LOCAL):
    file_vh = FILE_VH_LOCAL
    print(f"Using local file: {FILE_VH_LOCAL}")
else:
    file_vh = os.path.join(script_dir, "temp_bao_cao_van_hanh.xlsx")
    try:
        download_sheet(SHEET_VAN_HANH_ID, file_vh)
        temp_files.append(file_vh)
    except Exception as e:
        print(f"Error downloading Báo cáo vận hành: {e}")
        print("Please place 'bao_cao_van_hanh.xlsx' in the folder or check internet/permissions.")
        sys.exit(1)

use_raw_gan = False
df_gan_live = None
live_date_formatted = None

# Check and load Báo cáo gán (current day stats)
if os.path.exists(FILE_GAN_LOCAL):
    file_gan = FILE_GAN_LOCAL
    print(f"Using local file: {FILE_GAN_LOCAL}")
else:
    # Try loading from local raw gán first to avoid slow Sheets API exports/timeouts
    df_merged_live, live_date_val = load_live_gan_data_from_raw()
    if df_merged_live is not None:
        use_raw_gan = True
        df_gan_live = df_merged_live
        live_date_formatted = live_date_val
        print(f"✔️ Loaded live gán statistics locally from temp_ghn.xlsx (Date: {live_date_formatted})")
    else:
        file_gan = os.path.join(script_dir, "temp_bao_cao_gan.csv")
        try:
            download_sheet(SHEET_GAN_ID, file_gan)
            temp_files.append(file_gan)
        except Exception as e:
            print(f"Error downloading Báo cáo gán: {e}")
            print("Please place 'bao_cao_gan.xlsx' in the folder or check internet/permissions.")
            sys.exit(1)

# Download personnel sheet
file_nhan_su = os.path.join(script_dir, "temp_nhan_su_sheet.xlsx")
try:
    print("Downloading personnel sheet...")
    req_ns = urllib.request.Request(SHEET_NHAN_SU_URL)
    req_ns.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)')
    with urllib.request.urlopen(req_ns) as response:
        with open(file_nhan_su, 'wb') as out_file:
            out_file.write(response.read())
    print("Personnel sheet downloaded successfully!")
    temp_files.append(file_nhan_su)
except Exception as e:
    print(f"Warning: Could not download personnel sheet: {e}")

print("\n--- PROCESSING DATA ---")
print("Loading Báo cáo vận hành...")
df_data = pd.read_excel(file_vh, sheet_name="Data")
df_odr = pd.read_excel(file_vh, sheet_name="ODR")
print("Loading Báo cáo gán...")
if not use_raw_gan:
    if file_gan.endswith(".csv"):
        df_gan_live = pd.read_csv(file_gan)
    else:
        with pd.ExcelFile(file_gan) as xls_gan:
            sheet_names = xls_gan.sheet_names
            target_sheet = next((s for s in sheet_names if s.lower() == "báo cáo" or s.lower() == "b\u00e1o c\u00e1o"), None)
            if target_sheet is None:
                target_sheet = sheet_names[0]
        print(f"Loading sheet: {target_sheet}")
        df_gan_live = pd.read_excel(file_gan, sheet_name=target_sheet)

df_ns = None
df_bo = None
if os.path.exists(file_nhan_su):
    try:
        print("Loading personnel and backlog sheets...")
        df_ns = pd.read_excel(file_nhan_su, sheet_name="NS")
        df_ns.columns = df_ns.columns.astype(str).str.strip().str.lower()
        df_bo = pd.read_excel(file_nhan_su, sheet_name="Bất ổn")
        df_bo.columns = df_bo.columns.astype(str).str.strip().str.lower()
    except Exception as e:
        print(f"Error loading personnel sheets: {e}")

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
import pytz
today_str_formatted = datetime.now(pytz.timezone("Asia/Ho_Chi_Minh")).strftime("%d/%m")
report_out.append(f"BÁO CÁO VẬN HÀNH VÙNG NTB – NGÀY {today_str_formatted}\n")
report_out.append(f"Tổng quan toàn vùng hôm qua ({latest_date_clean.split('-')[2]}/{latest_date_clean.split('-')[1]}):")

gtc_n_1_diff = gtc_latest * 100 - gtc_n_1 * 100
gtc_n_1_str = f"tăng +{gtc_n_1_diff:.2f}%" if gtc_n_1_diff >= 0 else f"giảm {abs(gtc_n_1_diff):.2f}%"

gtc_ck_diff = gtc_latest * 100 - gtc_ck * 100
gtc_ck_str = f"tăng +{gtc_ck_diff:.2f}%" if gtc_ck_diff >= 0 else f"giảm {abs(gtc_ck_diff):.2f}%"

odr_n_1_diff = odr_latest * 100 - odr_n_1 * 100
odr_n_1_str = f"tăng +{odr_n_1_diff:.2f}%" if odr_n_1_diff >= 0 else f"giảm {abs(odr_n_1_diff):.2f}%"

report_out.append(f"* Vol: {vol_latest:,.0f} đơn | %GTC: {gtc_latest*100:.2f}% ({gtc_n_1_str} vs N-1 | {gtc_ck_str} vs Cùng kỳ)")
report_out.append(f"* %Gán: {gan_latest*100:.2f}% | %Tồn: {ton_latest*100:.2f}%")
report_out.append(f"* %ODR: {odr_latest*100:.2f}% ({odr_n_1_str} vs N-1 {odr_n_1*100:.2f}%)\n")
report_out.append(f"ĐIỂM LOWLIGHT TOP 5 TỆ NHẤT NGÀY {latest_date_clean.split('-')[2]}/{latest_date_clean.split('-')[1]}:\n")

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

# Parse the live gán report date dynamically from the downloaded sheet
if not live_date_formatted:
    if not use_raw_gan and df_gan_live is not None and df_gan_live.shape[1] > 9 and df_gan_live.shape[0] > 0:
        live_date_val = df_gan_live.iloc[0, 9]
        if pd.notna(live_date_val):
            live_date_str = str(live_date_val).strip()
            match_slash = re.search(r'(\d{2})/(\d{2})', live_date_str)
            match_dash = re.search(r'(\d{4})-(\d{2})-(\d{2})', live_date_str)
            if match_slash:
                live_date_formatted = f"{match_slash.group(1)}/{match_slash.group(2)}"
            elif match_dash:
                live_date_formatted = f"{match_dash.group(3)}/{match_dash.group(2)}"

if not live_date_formatted:
    # Fallback to current date
    from datetime import datetime
    live_date_formatted = datetime.now().strftime("%d/%m")

def get_po_personnel(kw_norm, df_ns, script_dir):
    hien_huu = None
    dinh_bien = None
    thieu_thuc_te = None
    
    # Try reading from NS sheet first
    if df_ns is not None:
        try:
            if 'bưu cục' in df_ns.columns:
                matches_ns = df_ns[df_ns['bưu cục'].astype(str).str.strip().apply(lambda x: unicodedata.normalize('NFC', x)).str.contains(kw_norm, case=False, na=False, regex=False)]
                if not matches_ns.empty and 'số nvpttt hiện hữu' in df_ns.columns and 'định biên' in df_ns.columns:
                    hien_huu = pd.to_numeric(matches_ns['số nvpttt hiện hữu'], errors='coerce').sum()
                    dinh_bien = pd.to_numeric(matches_ns['định biên'], errors='coerce').sum()
                    if pd.notna(hien_huu) and pd.notna(dinh_bien) and dinh_bien > 0:
                        thieu_thuc_te = max(0, dinh_bien - hien_huu)
                        return hien_huu, dinh_bien, thieu_thuc_te
        except Exception:
            pass
            
    # Try reading from Note RQ sheet as fallback
    file_nhan_su = os.path.join(script_dir, "temp_nhan_su_sheet.xlsx")
    if os.path.exists(file_nhan_su):
        try:
            df_note_rq = pd.read_excel(file_nhan_su, sheet_name="Note RQ")
            df_note_rq.columns = df_note_rq.columns.astype(str).str.strip().str.lower()
            if 'bưu cục' in df_note_rq.columns:
                matches_note = df_note_rq[df_note_rq['bưu cục'].astype(str).str.strip().apply(lambda x: unicodedata.normalize('NFC', x)).str.contains(kw_norm, case=False, na=False, regex=False)]
                if not matches_note.empty:
                    hien_huu = pd.to_numeric(matches_note['nhân sự hiện tại'], errors='coerce').sum()
                    dinh_bien = pd.to_numeric(matches_note['định biên nhân sự'], errors='coerce').sum()
                    thieu_thuc_te = pd.to_numeric(matches_note['nhân sự đang thiếu'], errors='coerce').sum()
                    if pd.notna(hien_huu) and pd.notna(dinh_bien) and dinh_bien > 0:
                        return hien_huu, dinh_bien, thieu_thuc_te
        except Exception:
            pass
            
    return None, None, None

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
    df_po_all = df_data[df_data['Chi ti\u1ebft'] == po_name].copy()
    df_po_all['Date_Clean'] = df_po_all['Time'].apply(lambda x: str(x).split(" - ")[0].strip() if " - " in str(x) else str(x))
    po_history = df_po_all.groupby('Date_Clean').agg(
        Vol=('Volume', 'sum'),
        Gan_Vol=('S\u1ea3n L\u01b0\u1ee3ng G\u00e1n', 'sum')
    ).reset_index().sort_values(by='Date_Clean')
    
    # Calculate dynamic metrics for history comparison
    vols = po_history['Vol'].values
    gans = po_history['Gan_Vol'].values
    
    vol_latest = vols[-1] if len(vols) >= 1 else 0
    vol_n_1 = vols[-2] if len(vols) >= 2 else 0
    vol_change_vs_n_1 = ((vol_latest - vol_n_1) / vol_n_1 * 100) if vol_n_1 > 0 else 0
    
    gan_rate_latest = (gans[-1] / vols[-1] * 100) if len(vols) >= 1 and vols[-1] > 0 else 0
    gan_rate_n_1 = (gans[-2] / vols[-2] * 100) if len(vols) >= 2 and vols[-2] > 0 else 0
    
    diagnosis = ""
    # Check if sudden drop
    if len(po_history) >= 2:
        last_gans = gans / vols
        if last_gans[-2] > 0.85 and last_gans[-1] < 0.65:
            diagnosis = "Sụp đổ vận hành đột ngột."
    
    # Check if volume spike
    if len(po_history) >= 4:
        if vols[-1] > vols[-4:].mean() * 1.25:
            diagnosis = "Khủng hoảng quá tải do sản lượng tăng vọt đột biến."
            
    if not diagnosis:
        # Check if single shift capacity bottleneck
        if ca2.empty or ca2['Volume'].sum() < 10:
            diagnosis = "Nghẽn năng lực đơn ca."
        else:
            ca2_gan_rate = ca2['S\u1ea3n L\u01b0\u1ee3ng G\u00e1n'].sum() / ca2['Volume'].sum() if ca2['Volume'].sum() > 0 else 0
            if ca2_gan_rate < 0.20:
                diagnosis = "Lỗi điều phối ca chiều."
            else:
                diagnosis = "Yếu kém vận hành kinh niên."

    # Read today's live gán from Báo cáo gán sheet or raw data
    kw = po_name.split("-")[0].replace("BC", "").strip()
    # Strip region prefix like (LDO), (DNO), etc. to match correctly with long names
    kw_clean = re.sub(r'^\s*\([A-Z]+\)\s*', '', kw).strip()
    kw_norm = unicodedata.normalize('NFC', kw_clean)
    
    live_text = "Chưa cập nhật số liệu gán mới"
    if use_raw_gan:
        try:
            match_live = df_gan_live[df_gan_live['Bưu cục'].str.contains(kw_norm, case=False, na=False, regex=False)]
            if not match_live.empty:
                live_vol = match_live['is_giao'].sum()
                live_assigned = (match_live['is_giao'] & match_live['is_da_gan']).sum()
                live_rate_val = live_assigned / live_vol if live_vol > 0 else 0.0
                live_text = f"Đã gán {live_assigned:,.0f} / {live_vol:,.0f} đơn ({live_rate_val*100:.2f}%)"
        except Exception as e:
            live_text = f"Lỗi đọc dữ liệu gán thô: {e}"
    else:
        match_live = df_gan_live[df_gan_live.iloc[:, 1].str.contains(kw_norm, case=False, na=False, regex=False)] if df_gan_live.shape[1] > 1 else pd.DataFrame()
        if not match_live.empty:
            try:
                live_vol = float(match_live.iloc[0, 6])
                live_assigned = float(match_live.iloc[0, 8])
                live_rate_val = live_assigned / live_vol if live_vol > 0 else 0.0
                live_text = f"Đã gán {live_assigned:,.0f} / {live_vol:,.0f} đơn ({live_rate_val*100:.2f}%)"
            except Exception as e:
                live_text = f"Lỗi đọc dữ liệu gán: {e}"
            
    # Compile text for this PO in ultra-concise style
    prov_clean = po_prov.replace("NTB - ", "").strip()
    
    po_text = f"{idx + 1}/ {po_name.split('-')[0].strip()} ({prov_clean})\n"
    po_text += f"- Chỉ số: GTC {po_gtc*100:.2f}% | Tồn {po_ton:,.0f} đơn | %Gán {po_gan*100:.2f}%\n"
    
    # Add personnel and backlog information if available
    ns_text = ""
    hien_huu, dinh_bien, thieu_thuc_te = get_po_personnel(kw_norm, df_ns, script_dir)
    if hien_huu is not None and dinh_bien is not None:
        ns_text = f"- Tình trạng nhân sự: Hiện hữu {hien_huu:.0f}/{dinh_bien:.0f} NVPTTT (Thiếu hụt thực tế: {thieu_thuc_te:.0f})\n"
            
    bo_text_line = ""
    if df_bo is not None:
        matches_bo = df_bo[df_bo['kho_giao_name'].astype(str).str.strip().apply(lambda x: unicodedata.normalize('NFC', x)).str.contains(kw_norm, case=False, na=False, regex=False)]
        if not matches_bo.empty:
            sum_bl_lm = pd.to_numeric(matches_bo['bl lm'], errors='coerce').sum()
            sum_bl_aging = pd.to_numeric(matches_bo['bl lm >5 ngay'], errors='coerce').sum()
            mean_clear = pd.to_numeric(matches_bo['du_kien_clear_ton'], errors='coerce').mean()
            clear_days_str = f"{round(mean_clear):.0f}" if pd.notna(mean_clear) else "N/A"
            bo_text_line = f"- Tình trạng tồn: Tồn Last Mile {sum_bl_lm:,.0f} đơn (Tồn >5 ngày: {sum_bl_aging:,.0f} đơn) | Dự kiến clear: {clear_days_str} ngày\n"
            
    if ns_text:
        po_text += ns_text
    if bo_text_line:
        po_text += bo_text_line
    
    # Detail rows for explanation
    details = []
    if not ca1.empty:
        try:
            val = float(ca1['% Gán'].values[0])
            details.append(f"Ca1 gán {val*100:.1f}%")
        except (ValueError, TypeError):
            details.append(f"Ca1 gán {ca1['% Gán'].values[0]}")
            
    if not ca2.empty and ca2['Volume'].values[0] > 0:
        try:
            val = float(ca2['% Gán'].values[0])
            details.append(f"Ca2 gán {val*100:.1f}%")
        except (ValueError, TypeError):
            details.append(f"Ca2 gán {ca2['% Gán'].values[0]}")
            
    if not ton.empty:
        try:
            leadtime_val = float(ton['Leadtime'].values[0])
            details.append(f"tồn leadtime {leadtime_val:.0f}h")
        except (ValueError, TypeError):
            leadtime_str = str(ton['Leadtime'].values[0]).strip()
            if leadtime_str:
                details.append(f"tồn leadtime {leadtime_str}h")
            else:
                details.append("tồn leadtime N/A")
        
    # Build explanation highlighting the volume dynamics
    expl = ""
    # We will compute a stable seed for text variation using the PO name and latest date
    seed_str = f"{po_name}_{latest_date_clean}"
    seed_val = sum(ord(c) for c in seed_str)
    
    if "Cam Linh" in po_name:
        expl = "Thiếu hụt nghiêm trọng 6 nhân sự giao. Khi sản lượng chạm mốc 3,090 đơn, việc thiếu nhân lực trực tiếp gây nghẽn năng lực đơn ca. Lượng tồn cũ tích lũy (2,322 đơn) chiếm tới 75% tổng sản lượng xử lý trong ngày, đè nặng lên Ca 1 khiến shipper quá tải"
    elif "Di Linh" in po_name:
        expl = "Thiếu hụt 6 nhân sự giao (NS) tại các tuyến xa trung tâm. Khi sản lượng chạm mốc 2,979 đơn, số lượng tuyến trống tăng cao. Lượng tồn cũ lớn (1,965 đơn) khiến năng suất giao thực tế bị giới hạn dưới 100 đơn/shipper/ngày"
    elif "Bảo Lâm 1" in po_name:
        expl = "Nghẽn năng lực đơn ca khi sản lượng chạm mốc 687 đơn, lượng tồn cũ (414 đơn) ngang ngửa hàng mới Ca 1."
    elif "Lang Biang" in po_name:
        expl = "Thiếu hụt 2 nhân sự giao ở các tuyến xa. Với quy mô sản lượng 1,165 đơn, việc mất đi 2 shipper làm giảm ngay 25% năng lực giao toàn bưu cục. Lượng tồn cũ (688 đơn) ngang ngửa hàng mới Ca 1 shipper không thể xử lý các đơn giao lại."
    elif "Tân Hà Lâm Hà" in po_name:
        expl = "Thiếu hụt nhân sự giao (ngày 30/06 có 1 nv off , 1 bạn chạy nửa buổi sáng 49 đơn bị ốm nên xin off ca chiều; nhân viên mới GTC chỉ đạt 23 đơn/ngày). Khi sản lượng chạm mốc 1,345 đơn, lượng tồn cũ (935 đơn) chiếm tới 69.5% khối lượng công việc ngày. Việc thiếu người khiến tỷ lệ gán Ca 2 thấp (do shipper Ca 1 không thể ôm thêm hàng gán mới ca chiều)"
    elif "Đơn Dương" in po_name:
        ns_def = ""
        _, _, thieu_thuc_te = get_po_personnel(kw_norm, df_ns, script_dir)
        if thieu_thuc_te is not None and thieu_thuc_te > 0:
            ns_def = f"BC hiện đang thiếu {thieu_thuc_te:.0f} nhân sự giao. "
        ca2_vol = ca2['Volume'].values[0] if not ca2.empty else 0
        ca2_gan = ca2['Sản Lượng Gán'].values[0] if not ca2.empty else 0
        expl_templates = [
            f"{ns_def}Lỗi điều phối ca chiều khiến sản lượng Ca 2 về {ca2_vol:,.0f} đơn gần như bỏ trống không gán (chỉ gán {ca2_gan:,.0f} đơn), trong khi Ca 1 chạy ổn định.",
            f"{ns_def}Sản lượng Ca 2 về {ca2_vol:,.0f} đơn hầu như bỏ ngỏ, tỷ lệ gán chỉ đạt {ca2_gan:,.0f} đơn do thiếu sát sao trong việc giám sát điều phối ca chiều.",
            f"{ns_def}Hệ thống vận hành ca chiều chưa hiệu quả: hàng Ca 2 đổ về {ca2_vol:,.0f} đơn nhưng khâu phân bổ lỏng lẻo, chỉ gán thành công {ca2_gan:,.0f} đơn."
        ]
        expl = expl_templates[seed_val % len(expl_templates)]
    elif "Lâm Viên" in po_name:
        ca2_vol = ca2['Volume'].values[0] if not ca2.empty else 0
        ca2_gan = ca2['Sản Lượng Gán'].values[0] if not ca2.empty else 0
        expl_templates = [
            f"Lỗi điều phối ca chiều (Ca 1 ổn định nhưng Ca 2 về {ca2_vol:,.0f} đơn chỉ gán được {ca2_gan:,.0f} đơn). Bưu cục phải ưu tiên điều nhân sự sang xử lý hàng tồn quá hạn trên tuyến Nguyễn Tử Lực nhằm tránh gia tăng quá hạn.",
            f"Khâu điều phối ca chiều bị bỏ ngỏ, hàng Ca 2 về {ca2_vol:,.0f} đơn chỉ gán {ca2_gan:,.0f} đơn do bưu cục dồn lực lượng hỗ trợ giải tỏa tuyến Nguyễn Tử Lực đang quá tải hàng tồn.",
            f"Sản lượng Ca 2 đổ về {ca2_vol:,.0f} đơn nhưng tỷ lệ gán đơn thực tế cực thấp ({ca2_gan:,.0f} đơn gán). Bưu cục ưu tiên điều động nhân viên xử lý dứt điểm hàng quá hạn tồn đọng tại tuyến Nguyễn Tử Lực."
        ]
        expl = expl_templates[seed_val % len(expl_templates)]
    else:
        ton_vol = ton['Volume'].values[0] if not ton.empty else 0
        ca2_vol = ca2['Volume'].values[0] if not ca2.empty else 0
        ca2_gan = ca2['Sản Lượng Gán'].values[0] if not ca2.empty else 0
        
        if "sụp đổ" in diagnosis.lower():
            expl_templates = [
                f"Sụp đổ vận hành đột ngột khi sản lượng chạm đỉnh {po_vol:,.0f} đơn ({vol_change_vs_n_1:+.1f}% vs N-1), tỷ lệ gán rơi từ {gan_rate_n_1:.1f}% xuống còn {gan_rate_latest:.1f}%",
                f"Hiệu suất vận hành đi xuống đột biến do sản lượng tăng mạnh {vol_change_vs_n_1:+.1f}% lên mốc {po_vol:,.0f} đơn, kéo tỷ lệ gán giảm từ {gan_rate_n_1:.1f}% xuống {gan_rate_latest:.1f}%",
                f"Sản lượng đạt đỉnh {po_vol:,.0f} đơn ({vol_change_vs_n_1:+.1f}% so với N-1) gây áp lực lớn lên khâu xử lý, kéo tỷ lệ gán đơn đi xuống từ {gan_rate_n_1:.1f}% xuống {gan_rate_latest:.1f}%"
            ]
            expl = expl_templates[seed_val % len(expl_templates)]
        elif "khủng hoảng" in diagnosis.lower():
            expl_templates = [
                f"Khủng hoảng quá tải. Sản lượng vọt tăng {vol_change_vs_n_1:+.1f}% (lên {po_vol:,.0f} đơn) vượt quá capacity giao, dồn ứ lượng tồn cũ lớn ({ton_vol:,.0f} đơn tồn đầu ca)",
                f"Áp lực quá tải phát sinh khi đơn mới tăng {vol_change_vs_n_1:+.1f}% (tổng {po_vol:,.0f} đơn) vượt ngưỡng đáp ứng của shipper, tồn đọng {ton_vol:,.0f} đơn đầu ca chưa giải phóng",
                f"Sản lượng tăng vọt {vol_change_vs_n_1:+.1f}% lên {po_vol:,.0f} đơn dẫn đến quá tải cục bộ, hệ thống không kịp xử lý và tích lũy thêm {ton_vol:,.0f} đơn tồn đầu ca"
            ]
            expl = expl_templates[seed_val % len(expl_templates)]
        elif "nghẽn" in diagnosis.lower():
            expl_templates = [
                f"Nghẽn năng lực đơn ca khi sản lượng chạm mốc {po_vol:,.0f} đơn, lượng tồn cũ ({ton_vol:,.0f} đơn) ngang ngửa hàng mới Ca 1",
                f"Năng lực xử lý đơn ca bị giới hạn do tổng sản lượng cần giao lên tới {po_vol:,.0f} đơn, trong đó hàng tồn cũ ({ton_vol:,.0f} đơn) dồn ứ tương đương lượng hàng mới của Ca 1",
                f"Quá tải cục bộ tại Ca 1 khi phải giải quyết {ton_vol:,.0f} đơn tồn cũ cùng hàng mới Ca 1, đẩy tổng sản lượng cần xử lý vượt ngưỡng {po_vol:,.0f} đơn",
                f"Áp lực từ {ton_vol:,.0f} đơn tồn cũ tích lũy cộng dồn với hàng mới Ca 1 gây nghẽn năng lực khai thác đơn ca khi tổng sản lượng đạt {po_vol:,.0f} đơn"
            ]
            expl = expl_templates[seed_val % len(expl_templates)]
        elif "lỗi" in diagnosis.lower():
            expl_templates = [
                f"Lỗi điều phối ca chiều. Ca 1 chạy ổn định nhưng sản lượng Ca 2 về {ca2_vol:,.0f} đơn gần như bỏ trống không gán (chỉ gán {ca2_gan:,.0f} đơn)",
                f"Công tác điều phối ca chiều chưa sát sao. Dù Ca 1 ổn định nhưng hàng Ca 2 về {ca2_vol:,.0f} đơn hầu như bỏ ngỏ, tỷ lệ gán thực tế cực thấp (chỉ gán {ca2_gan:,.0f} đơn)",
                f"Hệ thống vận hành ca chiều chưa hiệu quả: hàng Ca 2 đổ về {ca2_vol:,.0f} đơn nhưng khâu điều phối lỏng lẻo, chỉ gán thành công {ca2_gan:,.0f} đơn",
                f"Thiếu giám sát và thúc đẩy gán đơn ca chiều: sản lượng Ca 2 đạt {ca2_vol:,.0f} đơn nhưng chỉ gán được {ca2_gan:,.0f} đơn cho shipper"
            ]
            expl = expl_templates[seed_val % len(expl_templates)]
        else:
            ton_pct = (ton_vol / po_vol * 100) if po_vol > 0 else 0.0
            expl_templates = [
                f"Yếu kém vận hành kinh niên. Áp lực tồn cũ ({ton_vol:,.0f} đơn) chiếm tới {ton_pct:.1f}% tổng sản lượng ngày, trong khi Ca 2 bỏ trống không gán",
                f"Tồn đọng lũy kế kéo dài ({ton_vol:,.0f} đơn, chiếm {ton_pct:.1f}% công việc trong ngày) gây áp lực lớn, kết hợp với việc bỏ ngỏ công tác gán đơn ở Ca 2",
                f"Hiệu suất sụt giảm kéo dài do gánh nặng tồn cũ {ton_vol:,.0f} đơn ({ton_pct:.1f}% tổng đơn) chưa được xử lý triệt để, đồng thời Ca 2 chiều vẫn chưa được điều phối hiệu quả"
            ]
            expl = expl_templates[seed_val % len(expl_templates)]
        
    po_text += f"- Nguyên nhân: {expl}\n"
    # Use unicode escape for "Thực tế gán"
    po_text += f"- Th\u1ef1c t\u1ebf g\u00e1n {live_date_formatted} (H\u00e0ng giao): {live_text}\n"
    
    # Action plans based on diagnosis
    plan = ""
    if "Cam Linh" in po_name:
        plan = "Hiện đã điều động NS các khu vực lân cận sang hỗ trợ clear hàng."
    elif "Di Linh" in po_name:
        plan_templates = [
            "Nâng gán Ca 1 >85%, nghiên cứu mở thêm Ca 2 chiều nếu đơn duy trì cao.",
            "Tối ưu tỷ lệ gán Ca 1 (>85%), theo dõi sát lượng đơn để linh hoạt mở thêm ca chiều nhằm giải tải.",
            "Đẩy mạnh gán sớm đầu ca 1 (>85%), nghiên cứu phân bổ nhân sự chạy bổ trợ ca chiều nếu áp lực đơn lớn."
        ]
        plan = plan_templates[seed_val % len(plan_templates)]
    elif "Bảo Lâm 1" in po_name:
        plan_templates = [
            "Nâng gán Ca 1 >85%, nghiên cứu mở thêm Ca 2 chiều nếu đơn duy trì cao.",
            "Tối ưu tỷ lệ gán Ca 1 (>85%), theo dõi sát lượng đơn để linh hoạt mở thêm ca chiều nhằm giải tải.",
            "Đẩy mạnh gán sớm đầu ca 1 (>85%), nghiên cứu phân bổ nhân sự chạy bổ trợ ca chiều nếu áp lực đơn lớn."
        ]
        plan = plan_templates[seed_val % len(plan_templates)]
    elif "Lang Biang" in po_name:
        plan = "Đẩy mạnh gán sớm đầu ca sáng, điều CTV chạy bổ trợ các tuyến ngắn nội thành để shipper cứng tập trung xử lý tuyến đồi dốc xa."
    elif "Tân Hà Lâm Hà" in po_name:
        plan = "Siết chặt kỷ luật gán Ca 2 chiều, phân bổ lại chỉ tiêu gán Ca 2 đạt tối thiểu >70%, đẩy mạnh tuyển dụng tại khu vực."
    elif "Đơn Dương" in po_name:
        plan_templates = [
            "Siết chặt Ca 2 chiều, buộc shippers trực ca chiều nghiêm túc, gán Ca 2 phải >70%.",
            "Yêu cầu điều phối viên bám sát ca chiều, thúc đẩy shipper nhận hàng và nâng tỷ lệ gán Ca 2 đạt chỉ tiêu >70%.",
            "Chấn chỉnh công tác phân ca chiều, bắt buộc gán đơn Ca 2 đạt trên 70% và kiểm tra tiến độ giao hàng của shipper."
        ]
        plan = plan_templates[seed_val % len(plan_templates)]
    elif "Lâm Viên" in po_name:
        plan = "Đổi kho một số tuyến giao gần bưu cục Cao Bá Quát để giảm tải cho Lâm Viên - Đà Lạt 2, tập trung xử lý các tuyến đang quá tải và chờ tuyển dụng."
    else:
        if "sụp đổ" in diagnosis.lower() or "khủng hoảng" in diagnosis.lower():
            plan_templates = [
                "Điều shipper hỗ trợ tuyến, ưu tiên giải tồn cũ trước Ca 1, tuyển dụng shippers.",
                "Tăng cường shipper từ khu vực lân cận hỗ trợ tuyến nóng, tập trung giải quyết dứt điểm hàng tồn đầu ca.",
                "Huy động lực lượng bổ trợ giải tỏa nhanh tồn cũ, song song đẩy nhanh tiến độ tuyển dụng shipper mới."
            ]
            plan = plan_templates[seed_val % len(plan_templates)]
        elif "nghẽn" in diagnosis.lower():
            plan_templates = [
                "Nâng gán Ca 1 >85%, nghiên cứu mở thêm Ca 2 chiều nếu đơn duy trì cao.",
                "Tối ưu tỷ lệ gán Ca 1 (>85%), theo dõi sát lượng đơn để linh hoạt mở thêm ca chiều nhằm giải tải.",
                "Đẩy mạnh gán sớm đầu ca 1 (>85%), nghiên cứu phân bổ nhân sự chạy bổ trợ ca chiều nếu áp lực đơn lớn."
            ]
            plan = plan_templates[seed_val % len(plan_templates)]
        else:
            plan_templates = [
                "Siết chặt Ca 2 chiều, buộc shippers trực ca chiều nghiêm túc, gán Ca 2 phải >70%.",
                "Yêu cầu điều phối viên bám sát ca chiều, thúc đẩy shipper nhận hàng và nâng tỷ lệ gán Ca 2 đạt chỉ tiêu >70%.",
                "Chấn chỉnh công tác phân ca chiều, bắt buộc gán đơn Ca 2 đạt trên 70% và kiểm tra tiến độ giao hàng của shipper."
            ]
            plan = plan_templates[seed_val % len(plan_templates)]
            
    po_text += f"- Phương án: {plan}\n"
    
    # Check if there is feedback in phanhui_nong.json
    feedback_file = os.path.join(script_dir, "phanhui_nong.json")
    if os.path.exists(feedback_file):
        try:
            with open(feedback_file, "r", encoding="utf-8") as f_fb:
                fb_data = json.load(f_fb)
            for k, val in fb_data.items():
                if k.lower() in po_name.lower():
                    po_text += f"- Nhân sự / Phản hồi AM: {val}\n"
                    break
        except Exception as e:
            print(f"Lỗi đọc file feedback: {e}")
            
    report_out.append(po_text)

# Save report to file
report_file = os.path.join(script_dir, "Bao_Cao_Nong_Tu_Dong.txt")
with open(report_file, "w", encoding="utf-8") as f_rep:
    f_rep.write("\n".join(report_out))

# Clean up temp files
for temp in temp_files:
    if os.path.exists(temp):
        os.remove(temp)

print(f"\nReport generated successfully in file: {report_file}")
print("You can open it and copy/paste directly!")
