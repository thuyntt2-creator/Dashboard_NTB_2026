import os
import sys
import unicodedata
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Configure output encoding for Vietnamese characters
try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    pass

# Cấu hình đường dẫn lưu file ảnh (lưu thẳng ra Desktop của User)
DESKTOP_DIR = os.path.join(os.path.expanduser('~'), 'Desktop')
OVERALL_OUT_DIR = os.path.join(DESKTOP_DIR, 'Dashboard_Bao_Cao_Tong')

os.makedirs(OVERALL_OUT_DIR, exist_ok=True)

# Cấu hình Google Sheets
JSON_FILE = r'C:\Users\lap4all\Desktop\Backlog_Automation\credentials.json'
SHEET_ID = '1j6Xm7JRemUGRSfbL-wc8DMwt7qfR7j79w9q79_snVnU'
LOCAL_FILE = r'c:\Users\lap4all\Desktop\New folder\downloaded_user_sheet.xlsx'

# 1. Tải dữ liệu (Ưu tiên live Google Sheet -> Fallback sang file Excel cục bộ)
df_gtc_full, df_gtc_tts, df_ltc_full, df_ltc_tts, df_odr_full, df_odr_tts, df_cocau = None, None, None, None, None, None, None

try:
    print("🔄 Đang thử kết nối và tải dữ liệu mới nhất từ Google Sheets...")
    import gspread
    from google.oauth2.service_account import Credentials
    
    creds = Credentials.from_service_account_file(
        JSON_FILE, 
        scopes=['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
    )
    gc = gspread.authorize(creds)
    sh = gc.open_by_key(SHEET_ID)
    
    def get_df_from_sheet(sheet_name):
        ws = sh.worksheet(sheet_name)
        data = ws.get_all_values(value_render_option='UNFORMATTED_VALUE')
        if not data:
            return pd.DataFrame()
        return pd.DataFrame(data[1:], columns=data[0])
        
    df_gtc_full = get_df_from_sheet('dataGTC gốc full hàng')
    df_gtc_tts = get_df_from_sheet('dataGTC gốc TTS')
    df_ltc_full = get_df_from_sheet('dataLTC full hàng')
    df_ltc_tts = get_df_from_sheet('dataLTC TTS')
    df_odr_full = get_df_from_sheet('dataODRfull hàng ')
    df_odr_tts = get_df_from_sheet('dataODR TTS')
    df_cocau = get_df_from_sheet('cocau')
    print("✔️ Đọc dữ liệu trực tuyến thành công!")

except Exception as e:
    print(f"⚠️ Không thể kết nối tới Google Sheets ({e}). Đang chuyển sang đọc file Excel cục bộ...")
    if os.path.exists(LOCAL_FILE):
        df_gtc_full = pd.read_excel(LOCAL_FILE, sheet_name='dataGTC gốc full hàng')
        df_gtc_tts = pd.read_excel(LOCAL_FILE, sheet_name='dataGTC gốc TTS')
        df_ltc_full = pd.read_excel(LOCAL_FILE, sheet_name='dataLTC full hàng')
        df_ltc_tts = pd.read_excel(LOCAL_FILE, sheet_name='dataLTC TTS')
        df_odr_full = pd.read_excel(LOCAL_FILE, sheet_name='dataODRfull hàng ')
        df_odr_tts = pd.read_excel(LOCAL_FILE, sheet_name='dataODR TTS')
        df_cocau = pd.read_excel(LOCAL_FILE, sheet_name='cocau')
        print("✔️ Đọc dữ liệu cục bộ thành công!")
    else:
        print(f"❌ Lỗi: Không tìm thấy file cục bộ tại {LOCAL_FILE}.")
        sys.exit(1)

# 2. Xử lý và chuẩn hóa dữ liệu
def normalize_name(name):
    if pd.isna(name): return ""
    return unicodedata.normalize('NFC', str(name).strip()).upper()

df_cocau['BC_norm'] = df_cocau['BC'].apply(normalize_name)
bc_to_am = dict(zip(df_cocau['BC_norm'], df_cocau['Am']))
bc_to_tinh = dict(zip(df_cocau['BC_norm'], df_cocau['Tỉnh']))

def map_am(bc_name):
    return bc_to_am.get(normalize_name(bc_name), None)

def map_tinh(bc_name):
    return bc_to_tinh.get(normalize_name(bc_name), None)

def get_province_from_ql(ql):
    ql_str = str(ql)
    if 'Đắk Nông' in ql_str or 'Đăk Nông' in ql_str: return 'Đắk Nông'
    if 'Bình Thuận' in ql_str: return 'Bình Thuận'
    if 'Khánh Hòa' in ql_str: return 'Khánh Hòa'
    if 'Lâm Đồng' in ql_str: return 'Lâm Đồng'
    if 'Ninh Thuận' in ql_str: return 'Ninh Thuận'
    return None

# Ánh xạ thông tin AM/Tỉnh vào các bảng thô
for df in [df_gtc_full, df_gtc_tts, df_ltc_full, df_ltc_tts, df_odr_full, df_odr_tts]:
    if 'Chi tiết' in df.columns:
        df['AM_mapped'] = df['Chi tiết'].apply(map_am)
        df['Tỉnh_mapped'] = df['Chi tiết'].apply(map_tinh)
    if 'Quản lý' in df.columns:
        df['Tỉnh_mapped_ql'] = df['Quản lý'].apply(get_province_from_ql)
        df['Tỉnh_mapped'] = df['Tỉnh_mapped'].fillna(df['Tỉnh_mapped_ql'])

# Ép kiểu dữ liệu số
for df in [df_gtc_full, df_gtc_tts]:
    for col in ['Volume', '% Gán', '% GTC']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

for df in [df_ltc_full, df_ltc_tts]:
    for col in ['Volume', '%Gán', '%LTC']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

for df in [df_odr_full, df_odr_tts]:
    for col in ['GTC', '%Ontime']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

# Định nghĩa hàm cấu hình Matplotlib Light Theme
def setup_light_theme():
    plt.style.use('default')
    plt.rcParams['figure.facecolor'] = '#FFFFFF'
    plt.rcParams['axes.facecolor'] = '#FFFFFF'
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.sans-serif'] = ['Segoe UI', 'Roboto', 'Arial', 'sans-serif']
    plt.rcParams['text.color'] = '#1E293B'  # Slate 800
    plt.rcParams['axes.labelcolor'] = '#64748B'  # Slate 500
    plt.rcParams['xtick.color'] = '#64748B'
    plt.rcParams['ytick.color'] = '#64748B'

weeks_keys = ['2026/21', '2026/22', '2026/23', '2026/24']
weeks_label = ['W21', 'W22', 'W23', 'W24']
x = np.arange(len(weeks_label))

df_gtc_new = df_gtc_full[(df_gtc_full['Loại Hàng'].isin(['Hàng Mới Ca 1', 'Hàng Mới Ca 2'])) & (df_gtc_full['Chi tiết'] != 'Grand Total')]
df_tts_new = df_gtc_tts[(df_gtc_tts['Loại Hàng'].isin(['Hàng Mới Ca 1', 'Hàng Mới Ca 2'])) & (df_gtc_tts['Chi tiết'] != 'Grand Total')]

# =========================================================================
# HÀM VẼ DASHBOARD CARDS (TỔNG NTB)
# =========================================================================
def draw_dashboard_cards(output_path, title_prefix="", filter_am=None):
    setup_light_theme()
    
    df_gtc_f = df_gtc_new if filter_am is None else df_gtc_new[df_gtc_new['AM_mapped'] == filter_am]
    df_tts_f = df_tts_new if filter_am is None else df_tts_new[df_tts_new['AM_mapped'] == filter_am]
    
    if df_gtc_f.empty:
        return
        
    vols_tot = [df_gtc_f[df_gtc_f['Time'] == wk]['Volume'].sum() for wk in weeks_keys]
    vols_tts = [df_tts_f[df_tts_f['Time'] == wk]['Volume'].sum() for wk in weeks_keys]
    
    v_w23, v_w24 = vols_tot[2], vols_tot[3]
    pct_tot = (v_w24 - v_w23) / v_w23 if v_w23 > 0 else 0
    
    # Tính toán GTC
    gtc_tot_rates = []
    gtc_tts_rates = []
    for week in weeks_keys:
        sub_tot = df_gtc_full[(df_gtc_full['Loại Hàng'].isin(['Hàng Mới Ca 1', 'Hàng Mới Ca 2'])) & (df_gtc_full['Time'] == week) & (df_gtc_full['Chi tiết'] != 'Grand Total')]
        if filter_am: sub_tot = sub_tot[sub_tot['AM_mapped'] == filter_am]
        gtc_tot_rates.append((sub_tot['Volume'] * sub_tot['% GTC']).sum() / sub_tot['Volume'].sum() if not sub_tot.empty else 0)
        
        sub_tts = df_gtc_tts[(df_gtc_tts['Loại Hàng'].isin(['Hàng Mới Ca 1', 'Hàng Mới Ca 2'])) & (df_gtc_tts['Time'] == week) & (df_gtc_tts['Chi tiết'] != 'Grand Total')]
        if filter_am: sub_tts = sub_tts[sub_tts['AM_mapped'] == filter_am]
        gtc_tts_rates.append((sub_tts['Volume'] * sub_tts['% GTC']).sum() / sub_tts['Volume'].sum() if not sub_tts.empty else 0)
    
    diff_gtc = gtc_tot_rates[-1] - gtc_tot_rates[-2]
    
    # Tính toán LTC
    ltc_tot_rates = []
    ltc_tts_rates = []
    for week in weeks_keys:
        sub_tot = df_ltc_full[(df_ltc_full['Cấp quản lý'] != 'Grand Total') & (df_ltc_full['Time'] == week)]
        if filter_am: sub_tot = sub_tot[sub_tot['AM_mapped'] == filter_am]
        ltc_tot_rates.append((sub_tot['Volume'] * sub_tot['%Gán'] * sub_tot['%LTC']).sum() / (sub_tot['Volume'] * sub_tot['%Gán']).sum() if not sub_tot.empty else 0)
        
        sub_tts = df_ltc_tts[(df_ltc_tts['Cấp quản lý'] != 'Grand Total') & (df_ltc_tts['Time'] == week)]
        if filter_am: sub_tts = sub_tts[sub_tts['AM_mapped'] == filter_am]
        ltc_tts_rates.append((sub_tts['Volume'] * sub_tts['%Gán'] * sub_tts['%LTC']).sum() / (sub_tts['Volume'] * sub_tts['%Gán']).sum() if not sub_tts.empty else 0)
        
    diff_ltc = ltc_tot_rates[-1] - ltc_tot_rates[-2]

    # Tính toán ODR
    odr_tot_rates = []
    odr_tts_rates = []
    for week in weeks_keys:
        sub_tot = df_odr_full[df_odr_full['Time'] == week]
        if filter_am: sub_tot = sub_tot[sub_tot['AM_mapped'] == filter_am]
        odr_tot_rates.append((sub_tot['GTC'] * sub_tot['%Ontime']).sum() / sub_tot['GTC'].sum() if not sub_tot.empty else 0)
        
        sub_tts = df_odr_tts[df_odr_tts['Time'] == week]
        if filter_am: sub_tts = sub_tts[sub_tts['AM_mapped'] == filter_am]
        odr_tts_rates.append((sub_tts['GTC'] * sub_tts['%Ontime']).sum() / sub_tts['GTC'].sum() if not sub_tts.empty else 0)
        
    diff_odr = odr_tot_rates[-1] - odr_tot_rates[-2]

    # Tính toán ODR theo tỉnh cho biểu đồ Vùng
    df_odr_tot = df_odr_full.copy()
    df_odr_tot['Vol_Ontime'] = df_odr_tot['GTC'] * df_odr_tot['%Ontime']
    odr_grouped = df_odr_tot.groupby(['Tỉnh_mapped', 'Time']).agg(v=('GTC', 'sum'), vo=('Vol_Ontime', 'sum')).reset_index()
    odr_grouped['Pct_ODR'] = odr_grouped['vo'] / odr_grouped['v']
    provinces = odr_grouped['Tỉnh_mapped'].dropna().unique()
    colors = ['#3B82F6', '#EF4444', '#10B981', '#F59E0B', '#8B5CF6']

    # 1. Volume Card
    fig, ax = plt.subplots(figsize=(8, 5.2))
    fig.subplots_adjust(top=0.70, left=0.08, right=0.92, bottom=0.12)
    
    ax.plot(x, vols_tot, marker='o', linewidth=3.5, color='#4F46E5', mfc='white', mew=2.5, ms=8, label='Tổng Vùng NTB', zorder=4)
    ax.fill_between(x, vols_tot, color='#4F46E5', alpha=0.08)
    ax.plot(x, vols_tts, marker='o', linewidth=3.5, color='#06B6D4', mfc='white', mew=2.5, ms=8, label='Trong đó: Tuyến TTS', zorder=4)
    ax.fill_between(x, vols_tts, color='#06B6D4', alpha=0.08)
    
    title_vol = f"SẢN LƯỢNG GIAO TỔNG & TTS".upper()
    fig.text(0.06, 0.89, title_vol, fontsize=10, fontweight='bold', color='#64748B')
    fig.text(0.06, 0.77, f"{vols_tot[-1]:,f}".split('.')[0] + " đơn", fontsize=24, fontweight='bold', color='#0F172A')
    
    growth_color = '#15803D' if pct_tot >= 0 else '#B91C1C'
    badge_bg = '#DCFCE7' if pct_tot >= 0 else '#FEE2E2'
    arrow = '▲' if pct_tot >= 0 else '▼'
    fig.text(0.34, 0.78, f"{arrow} {pct_tot:+.2%} vs W23", fontsize=9.5, fontweight='bold', color=growth_color, 
             bbox=dict(facecolor=badge_bg, edgecolor='none', boxstyle='round,pad=0.3'))
    
    ax.set_ylim(0, max(vols_tot)*1.25)
    ax.set_xticks(x)
    ax.set_xticklabels(weeks_label, fontsize=10)
    ax.grid(axis='y', linestyle=':', alpha=0.6, color='#E2E8F0', zorder=0)
    for spine in ['top', 'right', 'left', 'bottom']:
        ax.spines[spine].set_visible(False)
    ax.legend(frameon=False, loc='upper left', fontsize=9, labelcolor='#475569')
    ax.annotate(f"{vols_tot[-1]:,.0f}", (x[-1], vols_tot[-1]), textcoords="offset points", xytext=(0,12), ha='center', fontweight='bold', color='#4F46E5')
    ax.annotate(f"{vols_tts[-1]:,.0f}", (x[-1], vols_tts[-1]), textcoords="offset points", xytext=(0,12), ha='center', fontweight='bold', color='#06B6D4')
    
    plt.savefig(os.path.join(output_path, "db_card_volume.png"), dpi=200, facecolor='#FFFFFF')
    plt.close()

    # 2. GTC Card
    fig, ax = plt.subplots(figsize=(8, 5.2))
    fig.subplots_adjust(top=0.70, left=0.08, right=0.92, bottom=0.12)
    
    ax.plot(x, [r * 100 for r in gtc_tot_rates], marker='o', linewidth=3.5, color='#4F46E5', mfc='white', mew=2.5, ms=8, label='GTC Tổng', zorder=4)
    ax.fill_between(x, [r * 100 for r in gtc_tot_rates], color='#4F46E5', alpha=0.08)
    ax.plot(x, [r * 100 for r in gtc_tts_rates], marker='o', linewidth=3.5, color='#F43F5E', mfc='white', mew=2.5, ms=8, label='GTC TTS', zorder=4)
    ax.fill_between(x, [r * 100 for r in gtc_tts_rates], color='#F43F5E', alpha=0.06)
    
    title_gtc = f"TỈ LỆ GIAO THÀNH CÔNG MỚI (GTC)".upper()
    fig.text(0.06, 0.89, title_gtc, fontsize=10, fontweight='bold', color='#64748B')
    fig.text(0.06, 0.77, f"{gtc_tot_rates[-1]:.2%}", fontsize=24, fontweight='bold', color='#0F172A')
    
    growth_color = '#15803D' if diff_gtc >= 0 else '#B91C1C'
    badge_bg = '#DCFCE7' if diff_gtc >= 0 else '#FEE2E2'
    arrow = '▲' if diff_gtc >= 0 else '▼'
    fig.text(0.24, 0.78, f"{arrow} {diff_gtc:+.2%} vs W23", fontsize=9.5, fontweight='bold', color=growth_color,
             bbox=dict(facecolor=badge_bg, edgecolor='none', boxstyle='round,pad=0.3'))
    
    ax.set_ylim(40, 85)
    ax.set_xticks(x)
    ax.set_xticklabels(weeks_label, fontsize=10)
    ax.grid(axis='y', linestyle=':', alpha=0.6, color='#E2E8F0', zorder=0)
    for spine in ['top', 'right', 'left', 'bottom']:
        ax.spines[spine].set_visible(False)
    ax.legend(frameon=False, loc='lower right', fontsize=9, labelcolor='#475569')
    for i, (t, s) in enumerate(zip(gtc_tot_rates, gtc_tts_rates)):
        ax.annotate(f'{t:.2%}', (x[i], t*100), textcoords="offset points", xytext=(0, 12), ha='center', fontweight='semibold', color='#4F46E5', fontsize=9.5)
        ax.annotate(f'{s:.2%}', (x[i], s*100), textcoords="offset points", xytext=(0, -20), ha='center', fontweight='semibold', color='#F43F5E', fontsize=9.5)
        
    plt.savefig(os.path.join(output_path, "db_card_gtc.png"), dpi=200, facecolor='#FFFFFF')
    plt.close()

    # 3. LTC Card
    fig, ax = plt.subplots(figsize=(8, 5.2))
    fig.subplots_adjust(top=0.70, left=0.08, right=0.92, bottom=0.12)
    
    ax.plot(x, [r * 100 for r in ltc_tot_rates], marker='o', linewidth=3.5, color='#10B981', mfc='white', mew=2.5, ms=8, label='LTC Tổng', zorder=4)
    ax.fill_between(x, [r * 100 for r in ltc_tot_rates], color='#10B981', alpha=0.08)
    ax.plot(x, [r * 100 for r in ltc_tts_rates], marker='o', linewidth=3.5, color='#F59E0B', mfc='white', mew=2.5, ms=8, label='LTC TTS', zorder=4)
    ax.fill_between(x, [r * 100 for r in ltc_tts_rates], color='#F59E0B', alpha=0.06)
    
    title_ltc = f"TỈ LỆ LẤY THÀNH CÔNG (LTC)".upper()
    fig.text(0.06, 0.89, title_ltc, fontsize=10, fontweight='bold', color='#64748B')
    fig.text(0.06, 0.77, f"{ltc_tot_rates[-1]:.2%}", fontsize=24, fontweight='bold', color='#0F172A')
    
    growth_color = '#15803D' if diff_ltc >= 0 else '#B91C1C'
    badge_bg = '#DCFCE7' if diff_ltc >= 0 else '#FEE2E2'
    arrow = '▲' if diff_ltc >= 0 else '▼'
    fig.text(0.24, 0.78, f"{arrow} {diff_ltc:+.2%} vs W23", fontsize=9.5, fontweight='bold', color=growth_color,
             bbox=dict(facecolor=badge_bg, edgecolor='none', boxstyle='round,pad=0.3'))
    
    ax.set_ylim(80, 100)
    ax.set_xticks(x)
    ax.set_xticklabels(weeks_label, fontsize=10)
    ax.grid(axis='y', linestyle=':', alpha=0.6, color='#E2E8F0', zorder=0)
    for spine in ['top', 'right', 'left', 'bottom']:
        ax.spines[spine].set_visible(False)
    ax.legend(frameon=False, loc='lower right', fontsize=9, labelcolor='#475569')
    for i, (t, s) in enumerate(zip(ltc_tot_rates, ltc_tts_rates)):
        ax.annotate(f'{t:.2%}', (x[i], t*100), textcoords="offset points", xytext=(0, 12), ha='center', fontweight='semibold', color='#10B981', fontsize=9.5)
        ax.annotate(f'{s:.2%}', (x[i], s*100), textcoords="offset points", xytext=(0, -20), ha='center', fontweight='semibold', color='#F59E0B', fontsize=9.5)
        
    plt.savefig(os.path.join(output_path, "db_card_ltc.png"), dpi=200, facecolor='#FFFFFF')
    plt.close()

    # 4. ODR Card
    fig, ax = plt.subplots(figsize=(8, 5.2))
    fig.subplots_adjust(top=0.72, left=0.08, right=0.92, bottom=0.12)
    
    for idx, prov in enumerate(provinces):
        sub = odr_grouped[odr_grouped['Tỉnh_mapped'] == prov]
        sub = sub.set_index('Time').reindex(weeks_keys).reset_index()
        rates = sub['Pct_ODR'].fillna(0) * 100
        ax.plot(x, rates, marker='o', linewidth=2.5, color=colors[idx % len(colors)], mfc='white', mew=2, ms=7, label=prov)
        if not rates.empty:
            val = rates.iloc[-1]
            ax.annotate(f'{val/100:.1%}', (x[-1], val), textcoords="offset points", xytext=(10, -3), ha='left', fontweight='semibold', color=colors[idx % len(colors)], fontsize=9)
    title_odr = f"TỈ LỆ GIAO ĐÚNG HẠN ODR THEO TỈNH VÙNG NTB".upper()
    legend_loc = 'lower left'
        
    fig.text(0.06, 0.89, title_odr, fontsize=10, fontweight='bold', color='#64748B')
    fig.text(0.06, 0.77, f"{odr_tot_rates[-1]:.2%}", fontsize=24, fontweight='bold', color='#0F172A')
    
    growth_color = '#15803D' if diff_odr >= 0 else '#B91C1C'
    badge_bg = '#DCFCE7' if diff_odr >= 0 else '#FEE2E2'
    arrow = '▲' if diff_odr >= 0 else '▼'
    fig.text(0.24, 0.78, f"{arrow} {diff_odr:+.2%} vs W23", fontsize=9.5, fontweight='bold', color=growth_color,
             bbox=dict(facecolor=badge_bg, edgecolor='none', boxstyle='round,pad=0.3'))
    
    ax.set_ylim(80, 100)
    ax.set_xticks(x)
    ax.set_xticklabels(weeks_label, fontsize=10)
    ax.grid(axis='y', linestyle=':', alpha=0.6, color='#E2E8F0', zorder=0)
    for spine in ['top', 'right', 'left', 'bottom']:
        ax.spines[spine].set_visible(False)
    ax.legend(frameon=False, loc=legend_loc, fontsize=9, labelcolor='#475569')
    
    plt.savefig(os.path.join(output_path, "db_card_odr.png"), dpi=200, facecolor='#FFFFFF')
    plt.close()

# =========================================================================
# CHẠY TẠO FILE CARDS & BIỂU ĐỒ SO SÁNH AM CONSOLIDATED
# =========================================================================

# 1. Tạo 4 card tổng cho Vùng NTB (Màu trắng)
print("📊 Đang tạo 4 card dashboard tổng (Nền trắng)...")
draw_dashboard_cards(OVERALL_OUT_DIR)
print(f"✔️ Đã lưu card tổng NTB vào thư mục: {OVERALL_OUT_DIR}")

# 2. Tạo 1 biểu đồ hợp nhất so sánh tất cả AM trên 1 hình ảnh duy nhất
print("\n📊 Đang vẽ biểu đồ so sánh hợp nhất tất cả AM (Volume, GTC, LTC, ODR) cho Tuần 24...")
try:
    week_key = '2026/24'
    
    # 1. Volume by AM
    df_gtc_w24 = df_gtc_full[(df_gtc_full['Loại Hàng'].isin(['Hàng Mới Ca 1', 'Hàng Mới Ca 2'])) & (df_gtc_full['Time'] == week_key) & (df_gtc_full['Chi tiết'] != 'Grand Total')].copy()
    am_vol = df_gtc_w24.groupby('AM_mapped')['Volume'].sum().reset_index()
    
    # 2. GTC rate by AM
    df_gtc_w24['Vol_GTC'] = df_gtc_w24['Volume'] * df_gtc_w24['% GTC']
    am_gtc_grouped = df_gtc_w24.groupby('AM_mapped').agg(v=('Volume', 'sum'), vg=('Vol_GTC', 'sum')).reset_index()
    am_gtc_grouped['% GTC'] = (am_gtc_grouped['vg'] / am_gtc_grouped['v']).fillna(0)
    
    # 3. LTC rate by AM
    df_ltc_w24 = df_ltc_full[(df_ltc_full['Cấp quản lý'] != 'Grand Total') & (df_ltc_full['Time'] == week_key)].copy()
    df_ltc_w24['Vol_Gan'] = df_ltc_w24['Volume'] * df_ltc_w24['%Gán']
    df_ltc_w24['Vol_LTC'] = df_ltc_w24['Volume'] * df_ltc_w24['%LTC']
    am_ltc_grouped = df_ltc_w24.groupby('AM_mapped').agg(v=('Volume', 'sum'), vl=('Vol_LTC', 'sum')).reset_index()
    am_ltc_grouped['% LTC'] = (am_ltc_grouped['vl'] / am_ltc_grouped['v']).fillna(0)

    
    # 4. ODR rate by AM
    df_odr_w24 = df_odr_full[(df_odr_full['Time'] == week_key) & (~df_odr_full['Quản lý'].astype(str).str.contains('Grand Total|Tổng cộng', case=False, na=False))].copy()
    df_odr_w24['Vol_Ontime'] = df_odr_w24['GTC'] * df_odr_w24['%Ontime']
    am_odr_grouped = df_odr_w24.groupby('AM_mapped').agg(v=('GTC', 'sum'), vo=('Vol_Ontime', 'sum')).reset_index()
    am_odr_grouped['% ODR'] = (am_odr_grouped['vo'] / am_odr_grouped['v']).fillna(0)
    
    # Merge
    all_ams = df_cocau['Am'].dropna().unique()
    metrics_df = pd.DataFrame({'AM': all_ams})
    metrics_df = metrics_df.merge(am_vol, left_on='AM', right_on='AM_mapped', how='left').drop(columns='AM_mapped').rename(columns={'Volume': 'Volume_W24'}).fillna(0)
    metrics_df = metrics_df.merge(am_gtc_grouped[['AM_mapped', '% GTC']], left_on='AM', right_on='AM_mapped', how='left').drop(columns='AM_mapped').rename(columns={'% GTC': 'GTC_W24'}).fillna(0)
    metrics_df = metrics_df.merge(am_ltc_grouped[['AM_mapped', '% LTC']], left_on='AM', right_on='AM_mapped', how='left').drop(columns='AM_mapped').rename(columns={'% LTC': 'LTC_W24'}).fillna(0)
    metrics_df = metrics_df.merge(am_odr_grouped[['AM_mapped', '% ODR']], left_on='AM', right_on='AM_mapped', how='left').drop(columns='AM_mapped').rename(columns={'% ODR': 'ODR_W24'}).fillna(0)
    
    # Bỏ các AM có sản lượng bằng 0
    metrics_df = metrics_df[metrics_df['Volume_W24'] > 0].copy()
    
    setup_light_theme()
    fig, axs = plt.subplots(2, 2, figsize=(20, 15))
    fig.patch.set_facecolor('#FFFFFF')
    
    # Subplot 1: Volume
    df_vol_sorted = metrics_df.sort_values(by='Volume_W24', ascending=False)
    ax = axs[0, 0]
    rects = ax.bar(df_vol_sorted['AM'], df_vol_sorted['Volume_W24'], color='#4F46E5', alpha=0.9, width=0.6)
    ax.set_title("SẢN LƯỢNG GIAO THEO AM (W24)", fontsize=13, fontweight='bold', pad=15)
    ax.set_ylabel("Sản lượng (đơn)", fontsize=10, fontweight='bold')
    ax.set_xticks(range(len(df_vol_sorted)))
    ax.set_xticklabels(df_vol_sorted['AM'], rotation=40, ha='right', fontsize=9.5)
    ax.grid(axis='y', linestyle=':', alpha=0.5, color='#CBD5E1')
    for spine in ['top', 'right', 'left']:
        ax.spines[spine].set_visible(False)
    ax.spines['bottom'].set_color('#CBD5E1')
    for rect in rects:
        h = rect.get_height()
        ax.annotate(f'{h:,.0f}', xy=(rect.get_x() + rect.get_width() / 2, h), xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=8, fontweight='bold', color='#3730A3')

    # Subplot 2: GTC
    df_gtc_sorted = metrics_df.sort_values(by='GTC_W24', ascending=False)
    ax = axs[0, 1]
    rects = ax.bar(df_gtc_sorted['AM'], df_gtc_sorted['GTC_W24'] * 100, color='#10B981', alpha=0.9, width=0.6)
    ax.set_title("TỶ LỆ GIAO THÀNH CÔNG (GTC) THEO AM (W24)", fontsize=13, fontweight='bold', pad=15)
    ax.set_ylabel("Tỷ lệ GTC (%)", fontsize=10, fontweight='bold')
    ax.set_xticks(range(len(df_gtc_sorted)))
    ax.set_xticklabels(df_gtc_sorted['AM'], rotation=40, ha='right', fontsize=9.5)
    ax.set_ylim(0, 110)
    ax.grid(axis='y', linestyle=':', alpha=0.5, color='#CBD5E1')
    avg_gtc = (df_gtc_w24['Vol_GTC'].sum() / df_gtc_w24['Volume'].sum()) * 100
    ax.axhline(avg_gtc, color='#EF4444', linestyle='--', linewidth=1.5, label=f'Bình quân vùng ({avg_gtc:.1f}%)')
    ax.legend(frameon=False, loc='upper right', fontsize=9.5)
    for spine in ['top', 'right', 'left']:
        ax.spines[spine].set_visible(False)
    ax.spines['bottom'].set_color('#CBD5E1')
    for rect in rects:
        h = rect.get_height()
        ax.annotate(f'{h:.1f}%', xy=(rect.get_x() + rect.get_width() / 2, h), xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=8, fontweight='bold', color='#065F46')

    # Subplot 3: LTC
    df_ltc_sorted = metrics_df.sort_values(by='LTC_W24', ascending=False)
    ax = axs[1, 0]
    rects = ax.bar(df_ltc_sorted['AM'], df_ltc_sorted['LTC_W24'] * 100, color='#06B6D4', alpha=0.9, width=0.6)
    ax.set_title("TỶ LỆ LẤY THÀNH CÔNG (LTC) THEO AM (W24)", fontsize=13, fontweight='bold', pad=15)
    ax.set_ylabel("Tỷ lệ LTC (%)", fontsize=10, fontweight='bold')
    ax.set_xticks(range(len(df_ltc_sorted)))
    ax.set_xticklabels(df_ltc_sorted['AM'], rotation=40, ha='right', fontsize=9.5)
    ax.set_ylim(0, 110)
    ax.grid(axis='y', linestyle=':', alpha=0.5, color='#CBD5E1')
    avg_ltc = (df_ltc_w24['Vol_LTC'].sum() / df_ltc_w24['Volume'].sum()) * 100
    ax.axhline(avg_ltc, color='#EF4444', linestyle='--', linewidth=1.5, label=f'Bình quân vùng ({avg_ltc:.1f}%)')

    ax.legend(frameon=False, loc='upper right', fontsize=9.5)
    for spine in ['top', 'right', 'left']:
        ax.spines[spine].set_visible(False)
    ax.spines['bottom'].set_color('#CBD5E1')
    for rect in rects:
        h = rect.get_height()
        ax.annotate(f'{h:.1f}%', xy=(rect.get_x() + rect.get_width() / 2, h), xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=8, fontweight='bold', color='#075985')

    # Subplot 4: ODR
    df_odr_sorted = metrics_df.sort_values(by='ODR_W24', ascending=False)
    ax = axs[1, 1]
    rects = ax.bar(df_odr_sorted['AM'], df_odr_sorted['ODR_W24'] * 100, color='#F59E0B', alpha=0.9, width=0.6)
    ax.set_title("TỶ LỆ GIAO ĐÚNG HẠN (ODR) THEO AM (W24)", fontsize=13, fontweight='bold', pad=15)
    ax.set_ylabel("Tỷ lệ ODR (%)", fontsize=10, fontweight='bold')
    ax.set_xticks(range(len(df_odr_sorted)))
    ax.set_xticklabels(df_odr_sorted['AM'], rotation=40, ha='right', fontsize=9.5)
    ax.set_ylim(0, 110)
    ax.grid(axis='y', linestyle=':', alpha=0.5, color='#CBD5E1')
    avg_odr = (df_odr_w24['Vol_Ontime'].sum() / df_odr_w24['GTC'].sum()) * 100
    ax.axhline(avg_odr, color='#EF4444', linestyle='--', linewidth=1.5, label=f'Bình quân vùng ({avg_odr:.1f}%)')
    ax.legend(frameon=False, loc='upper right', fontsize=9.5)
    for spine in ['top', 'right', 'left']:
        ax.spines[spine].set_visible(False)
    ax.spines['bottom'].set_color('#CBD5E1')
    for rect in rects:
        h = rect.get_height()
        ax.annotate(f'{h:.1f}%', xy=(rect.get_x() + rect.get_width() / 2, h), xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=8, fontweight='bold', color='#92400E')
        
    plt.suptitle("BẢNG SO SÁNH HIỆU SUẤT VẬN HÀNH GIỮA CÁC AREA MANAGER (TUẦN 24)", fontsize=16, fontweight='bold', color='#0F172A', y=0.98)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    
    comp_out_path = os.path.join(DESKTOP_DIR, "So_sanh_hieu_suat_cac_AM_W24.png")
    plt.savefig(comp_out_path, dpi=200, facecolor='#FFFFFF')
    plt.close()
    print(f"✔️ Đã lưu biểu đồ so sánh AM hợp nhất vào Desktop: {comp_out_path}")
except Exception as ce:
    print(f"❌ Lỗi vẽ biểu đồ so sánh AM: {ce}")

print("\n🎉 HOÀN THÀNH TẠO TOÀN BỘ DASHBOARD CARDS & BIỂU ĐỒ SO SÀNH AM HỢP NHẤT TRÊN DESKTOP!")
