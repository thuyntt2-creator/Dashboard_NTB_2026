import os
import sys
import unicodedata
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import gspread
from google.oauth2.service_account import Credentials

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

print("="*60)
print("BẮT ĐẦU CHẠY PIPELINE TỔNG HỢP: DASHBOARD AM & BÁO CÁO OPR TTS + RỚT LC")
print("="*60)

# 1. Tải dữ liệu (Ưu tiên live Google Sheet -> Fallback sang file Excel cục bộ)
df_gtc_full, df_gtc_tts, df_ltc_full, df_ltc_tts, df_odr_full, df_odr_tts, df_cocau = None, None, None, None, None, None, None
df_opr, df_lc = None, None

try:
    print("🔄 Đang thử kết nối và tải dữ liệu mới nhất từ Google Sheets...")
    creds = Credentials.from_service_account_file(
        JSON_FILE, 
        scopes=['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
    )
    gc = gspread.authorize(creds)
    sh = gc.open_by_key(SHEET_ID)
    
    def get_df_from_sheet(sheet_name):
        print(f"-> Đang tải dữ liệu thô từ sheet '{sheet_name}'...")
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
    df_opr = get_df_from_sheet('OPR TTS')
    df_lc = get_df_from_sheet('data rớt LC')
    if not df_lc.empty:
        df_lc = df_lc.iloc[:, :8]
    print("✔️ Đọc dữ liệu trực tuyến từ Google Sheets thành công!")

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
        df_opr = pd.read_excel(LOCAL_FILE, sheet_name='OPR TTS')
        df_lc = pd.read_excel(LOCAL_FILE, sheet_name='data rớt LC')
        if not df_lc.empty:
            df_lc = df_lc.iloc[:, :8]
        print("✔️ Đọc dữ liệu cục bộ từ Excel thành công!")
    else:
        print(f"❌ Lỗi: Không tìm thấy file cục bộ tại {LOCAL_FILE}.")
        sys.exit(1)

# 2. Xử lý dữ liệu cho phần Dashboard
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
# PHẦN 1: CHẠY TẠO DASHBOARD CARDS & BIỂU ĐỒ SO SÁNH AM CONSOLIDATED CỤC BỘ
# =========================================================================

# 1. Tạo 4 card tổng cho Vùng NTB (Màu trắng)
print("\n📊 Đang tạo 4 card dashboard tổng (Nền trắng)...")
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


# =========================================================================
# PHẦN 2: CHẠY TÍNH TOÁN OPR TTS & RỚT LC VÀ ĐỒNG BỘ LÊN GOOGLE SHEETS
# =========================================================================

if 'sh' in locals() and sh is not None:
    print("\n📊 Đang bắt đầu phần 2: Tính toán OPR TTS & Rớt LC và đồng bộ lên Google Sheets...")
    
    # Map AM robustly
    df_cocau['Bưu cục_norm'] = df_cocau['Bưu cục'].apply(normalize_name)
    df_cocau['BC_norm'] = df_cocau['BC'].apply(normalize_name)

    bc_to_am_robust = {}
    for _, r in df_cocau.iterrows():
        am_val = str(r['Am']).strip()
        bc_to_am_robust[r['BC_norm']] = am_val
    for _, r in df_cocau.iterrows():
        am_val = str(r['Am']).strip()
        bc_to_am_robust[r['Bưu cục_norm']] = am_val

    def map_am_robust(bc_name):
        norm = normalize_name(bc_name)
        if not norm:
            return "Unknown"
        if norm in bc_to_am_robust:
            return bc_to_am_robust[norm]
        for k, v in bc_to_am_robust.items():
            if k in norm or norm in k:
                return v
        return "Unknown"

    df_opr['mapped_AM'] = df_opr['kholay'].apply(map_am_robust)
    df_lc['mapped_AM'] = df_lc['Chi tiết'].apply(map_am_robust)

    # Clean numeric columns
    df_opr['vol_ltc'] = pd.to_numeric(df_opr['vol_ltc'], errors='coerce').fillna(0)
    df_opr['ot'] = pd.to_numeric(df_opr['ot'], errors='coerce').fillna(0)
    df_lc['Vol cần LC'] = pd.to_numeric(df_lc['Vol cần LC'], errors='coerce').fillna(0)

    def parse_pct(val):
        if pd.isna(val) or val == "":
            return 0.0
        if isinstance(val, (int, float)):
            return float(val)
        val_str = str(val).strip().replace('%', '')
        try:
            val_str = val_str.replace(',', '.')
            return float(val_str) / 100.0
        except:
            return 0.0
    df_lc['pct_float'] = df_lc['%_rot_lc'].apply(parse_pct)
    df_lc['Vol rớt LC'] = df_lc['Vol cần LC'] * df_lc['pct_float']

    # 1. OPR TTS Calculations
    print("-> Đang tính toán bảng tổng hợp OPR TTS...")
    df_opr_w24 = df_opr[df_opr['Tuần'] == 'W24'].copy()
    opr_grouped = df_opr_w24.groupby(['mapped_AM', 'Khung giờ']).agg(
        Tong_Don=('vol_ltc', 'sum'),
        Don_Dung_Han=('ot', 'sum')
    ).reset_index()
    opr_grouped['%OPR'] = (opr_grouped['Don_Dung_Han'] / opr_grouped['Tong_Don']).fillna(0)

    pivot_df_opr = opr_grouped.pivot(index='mapped_AM', columns='Khung giờ', values=['Tong_Don', 'Don_Dung_Han', '%OPR']).fillna(0)
    pivot_df_opr.columns = [f"{col[0]}_{'9h_19h' if '9h-19h' in col[1] else '19h_9h'}" for col in pivot_df_opr.columns]
    pivot_df_opr = pivot_df_opr.reset_index()
    pivot_df_opr = pivot_df_opr.sort_values(by='%OPR_9h_19h', ascending=False)

    opr_headers = [
        "AM", 
        "Tổng đơn (9h-19h)", "Đúng hạn (9h-19h)", "%OPR (9h-19h)",
        "Tổng đơn (19h-9h)", "Đúng hạn (19h-9h)", "%OPR (19h-9h)"
    ]
    opr_upload_rows = [opr_headers]
    for _, row in pivot_df_opr.iterrows():
        opr_upload_rows.append([
            row['mapped_AM'],
            int(row['Tong_Don_9h_19h']),
            int(row['Don_Dung_Han_9h_19h']),
            float(row['%OPR_9h_19h']),
            int(row['Tong_Don_19h_9h']),
            int(row['Don_Dung_Han_19h_9h']),
            float(row['%OPR_19h_9h'])
        ])

    # 2. Leftover LC (Rớt LC) Calculations
    print("-> Đang tính toán bảng tổng hợp Rớt LC...")
    lc_wow = df_lc[df_lc['Tuần'].isin(['Tuần 23', 'Tuần 24'])].groupby('Tuần').agg(
        Vol_Can=('Vol cần LC', 'sum'),
        Vol_Rot=('Vol rớt LC', 'sum')
    ).reset_index()
    lc_wow['% rớt LC'] = (lc_wow['Vol_Rot'] / lc_wow['Vol_Can']).fillna(0)
    lc_wow = lc_wow.sort_values(by='Tuần')

    lc_wow_rows = []
    w23_pct, w24_pct = 0.0, 0.0
    for _, row in lc_wow.iterrows():
        lc_wow_rows.append([
            row['Tuần'],
            int(round(row['Vol_Can'])),
            int(round(row['Vol_Rot'])),
            float(row['% rớt LC'])
        ])
        if row['Tuần'] == 'Tuần 23':
            w23_pct = row['% rớt LC']
        elif row['Tuần'] == 'Tuần 24':
            w24_pct = row['% rớt LC']

    diff_pct = w24_pct - w23_pct
    lc_wow_rows.append([
        "So sánh W24 vs W23 (Chênh lệch)",
        "",
        "",
        float(diff_pct)
    ])

    df_lc_w24 = df_lc[df_lc['Tuần'] == 'Tuần 24'].copy()
    po_grouped = df_lc_w24.groupby('Chi tiết').agg(
        Vol_Can=('Vol cần LC', 'sum'),
        Vol_Rot=('Vol rớt LC', 'sum')
    ).reset_index()
    po_grouped['% rớt LC'] = (po_grouped['Vol_Rot'] / po_grouped['Vol_Can']).fillna(0)
    top_20_po = po_grouped.sort_values(by='% rớt LC', ascending=False).head(20)

    lc_top20_rows = []
    for idx, (_, row) in enumerate(top_20_po.iterrows(), start=1):
        lc_top20_rows.append([
            idx,
            row['Chi tiết'],
            int(round(row['Vol_Can'])),
            int(round(row['Vol_Rot'])),
            float(row['% rớt LC'])
        ])

    # Ghi đè & định dạng trang tính Google Sheets
    def write_and_format_sheet(sheet_name, data, formats_callback):
        try:
            try:
                ws = sh.worksheet(sheet_name)
                sh.del_worksheet(ws)
                print(f"  -> Đã xóa sheet cũ '{sheet_name}'")
            except gspread.exceptions.WorksheetNotFound:
                pass
            
            num_rows = max(len(data) + 15, 60)
            num_cols = max(len(data[0]) + 15, 20)
            ws = sh.add_worksheet(title=sheet_name, rows=str(num_rows), cols=str(num_cols))
            ws.update(range_name='A1', values=data, value_input_option='USER_ENTERED')
            
            sh.batch_update({
                "requests": [{
                    "updateSheetProperties": {
                        "properties": {"sheetId": ws.id, "gridProperties": {"hideGridlines": False}},
                        "fields": "gridProperties.hideGridlines"
                    }
                }]
            })
            
            formats_callback(ws, len(data))
            print(f"  ✔️ Đã ghi & định dạng thành công sheet '{sheet_name}'")
            return ws.id
        except Exception as e:
            print(f"  ❌ Lỗi ghi/định dạng sheet '{sheet_name}': {e}")
            return None

    def format_opr_summary(ws, num_rows):
        ws.format("A1:G1", {
            "backgroundColor": {"red": 30/255, "green": 41/255, "blue": 59/255},
            "horizontalAlignment": "CENTER",
            "textFormat": {"foregroundColor": {"red": 1.0, "green": 1.0, "blue": 1.0}, "bold": True, "fontFamily": "Segoe UI", "fontSize": 11}
        })
        ws.format(f"A2:G{num_rows}", {"textFormat": {"fontFamily": "Segoe UI", "fontSize": 10}})
        ws.format(f"A2:A{num_rows}", {"horizontalAlignment": "LEFT"})
        ws.format(f"B2:C{num_rows}", {"horizontalAlignment": "RIGHT", "numberFormat": {"type": "NUMBER", "pattern": "#,##0"}})
        ws.format(f"D2:D{num_rows}", {"horizontalAlignment": "RIGHT", "numberFormat": {"type": "PERCENT", "pattern": "0.0%"}})
        ws.format(f"E2:F{num_rows}", {"horizontalAlignment": "RIGHT", "numberFormat": {"type": "NUMBER", "pattern": "#,##0"}})
        ws.format(f"G2:G{num_rows}", {"horizontalAlignment": "RIGHT", "numberFormat": {"type": "PERCENT", "pattern": "0.0%"}})
        
        requests = []
        for r in range(2, num_rows + 1):
            color = {"red": 248/255, "green": 250/255, "blue": 252/255} if r % 2 == 0 else {"red": 1.0, "green": 1.0, "blue": 1.0}
            requests.append({
                "repeatCell": {
                    "range": {"sheetId": ws.id, "startRowIndex": r-1, "endRowIndex": r, "startColumnIndex": 0, "endColumnIndex": 7},
                    "cell": {"userEnteredFormat": {"backgroundColor": color}},
                    "fields": "userEnteredFormat.backgroundColor"
                }
            })
        sh.batch_update({"requests": requests})

    def format_lc_summary(ws, num_rows):
        ws.format("A1", {"textFormat": {"bold": True, "fontFamily": "Segoe UI", "fontSize": 14, "foregroundColor": {"red": 15/255, "green": 23/255, "blue": 42/255}}})
        ws.format("A3", {"textFormat": {"bold": True, "fontFamily": "Segoe UI", "fontSize": 12, "foregroundColor": {"red": 30/255, "green": 41/255, "blue": 59/255}}})
        ws.format("A9", {"textFormat": {"bold": True, "fontFamily": "Segoe UI", "fontSize": 12, "foregroundColor": {"red": 30/255, "green": 41/255, "blue": 59/255}}})
        
        ws.format("A4:D4", {
            "backgroundColor": {"red": 30/255, "green": 41/255, "blue": 59/255},
            "horizontalAlignment": "CENTER",
            "textFormat": {"foregroundColor": {"red": 1.0, "green": 1.0, "blue": 1.0}, "bold": True, "fontFamily": "Segoe UI", "fontSize": 11}
        })
        ws.format("A5:D7", {"textFormat": {"fontFamily": "Segoe UI", "fontSize": 10}})
        ws.format("A5:A7", {"horizontalAlignment": "LEFT"})
        ws.format("B5:C7", {"horizontalAlignment": "RIGHT", "numberFormat": {"type": "NUMBER", "pattern": "#,##0"}})
        ws.format("D5:D7", {"horizontalAlignment": "RIGHT", "numberFormat": {"type": "PERCENT", "pattern": "0.00%"}})
        
        ws.format("A11:E11", {
            "backgroundColor": {"red": 30/255, "green": 41/255, "blue": 59/255},
            "horizontalAlignment": "CENTER",
            "textFormat": {"foregroundColor": {"red": 1.0, "green": 1.0, "blue": 1.0}, "bold": True, "fontFamily": "Segoe UI", "fontSize": 11}
        })
        ws.format("A12:E31", {"textFormat": {"fontFamily": "Segoe UI", "fontSize": 10}})
        ws.format("A12:A31", {"horizontalAlignment": "CENTER"})
        ws.format("B12:B31", {"horizontalAlignment": "LEFT"})
        ws.format("C12:D31", {"horizontalAlignment": "RIGHT", "numberFormat": {"type": "NUMBER", "pattern": "#,##0"}})
        ws.format("E12:E31", {"horizontalAlignment": "RIGHT", "numberFormat": {"type": "PERCENT", "pattern": "0.00%"}})
        
        ws.format("A7:D7", {
            "textFormat": {"bold": True, "foregroundColor": {"red": 220/255, "green": 38/255, "blue": 38/255}},
            "backgroundColor": {"red": 254/255, "green": 242/255, "blue": 242/255}
        })
        
        requests = []
        for r in range(12, 32):
            color = {"red": 248/255, "green": 250/255, "blue": 252/255} if r % 2 == 0 else {"red": 1.0, "green": 1.0, "blue": 1.0}
            requests.append({
                "repeatCell": {
                    "range": {"sheetId": ws.id, "startRowIndex": r-1, "endRowIndex": r, "startColumnIndex": 0, "endColumnIndex": 5},
                    "cell": {"userEnteredFormat": {"backgroundColor": color}},
                    "fields": "userEnteredFormat.backgroundColor"
                }
            })
        sh.batch_update({"requests": requests})

    # Ghi dữ liệu
    opr_ws_id = write_and_format_sheet('OPR TTS Summary', opr_upload_rows, format_opr_summary)

    lc_upload_rows = [
        ["BÁO CÁO TỔNG HỢP RỚT LC VÙNG NTB"],
        [],
        ["1. SO SÁNH SỐ LIỆU TỔNG HỢP VỚI TUẦN TRƯỚC (W23 vs W24)"],
        ["Tuần", "Tổng Vol cần LC", "Tổng Vol rớt LC", "% rớt LC"],
    ]
    lc_upload_rows.extend(lc_wow_rows)
    lc_upload_rows.extend([[], []])
    lc_upload_rows.append(["2. TOP 20 BƯU CỤC CÓ TỶ LỆ RỚT LC CAO NHẤT (TUẦN 24)"])
    lc_upload_rows.append(["STT", "Bưu cục (Chi tiết)", "Tổng Vol cần LC", "Tổng Vol rớt LC", "% rớt LC"])
    lc_upload_rows.extend(lc_top20_rows)

    lc_ws_id = write_and_format_sheet('Rớt LC Summary', lc_upload_rows, format_lc_summary)

    # Chèn biểu đồ online
    print("-> Đang chèn biểu đồ động (native charts) lên Google Sheets...")
    chart_requests = []
    if opr_ws_id:
        end_idx = len(opr_upload_rows)
        chart_requests.append({
            "addChart": {
                "chart": {
                    "spec": {
                        "title": "HIỆU SUẤT OPR TTS THEO AM VÀ KHUNG GIỜ (W24)",
                        "titleTextFormat": {"fontFamily": "Segoe UI", "fontSize": 14, "bold": True},
                        "basicChart": {
                            "chartType": "COLUMN",
                            "legendPosition": "BOTTOM_LEGEND",
                            "headerCount": 1,
                            "axis": [
                                {"position": "BOTTOM_AXIS", "title": "Area Manager (AM)"},
                                {"position": "LEFT_AXIS", "title": "Tỷ lệ OPR (%)"}
                            ],
                            "domains": [
                                {"domain": {"sourceRange": {"sources": [{"sheetId": opr_ws_id, "startRowIndex": 0, "endRowIndex": end_idx, "startColumnIndex": 0, "endColumnIndex": 1}]}}}
                            ],
                            "series": [
                                {"series": {"sourceRange": {"sources": [{"sheetId": opr_ws_id, "startRowIndex": 0, "endRowIndex": end_idx, "startColumnIndex": 3, "endColumnIndex": 4}]}}, "targetAxis": "LEFT_AXIS"},
                                {"series": {"sourceRange": {"sources": [{"sheetId": opr_ws_id, "startRowIndex": 0, "endRowIndex": end_idx, "startColumnIndex": 6, "endColumnIndex": 7}]}}, "targetAxis": "LEFT_AXIS"}
                            ]
                        }
                    },
                    "position": {
                        "overlayPosition": {
                            "anchorCell": {"sheetId": opr_ws_id, "rowIndex": 1, "columnIndex": 8},
                            "offsetXPixels": 20, "offsetYPixels": 0
                        }
                    }
                }
            }
        })

    if lc_ws_id:
        chart_requests.append({
            "addChart": {
                "chart": {
                    "spec": {
                        "title": "TOP 20 BƯU CỤC CÓ TỶ LỆ RỚT LC CAO NHẤT (W24)",
                        "titleTextFormat": {"fontFamily": "Segoe UI", "fontSize": 14, "bold": True},
                        "basicChart": {
                            "chartType": "BAR",
                            "legendPosition": "NO_LEGEND",
                            "headerCount": 1,
                            "axis": [
                                {"position": "BOTTOM_AXIS", "title": "Tỷ lệ rớt LC (%)"},
                                {"position": "LEFT_AXIS", "title": "Bưu cục"}
                            ],
                            "domains": [
                                {"domain": {"sourceRange": {"sources": [{"sheetId": lc_ws_id, "startRowIndex": 10, "endRowIndex": 31, "startColumnIndex": 1, "endColumnIndex": 2}]}}}
                            ],
                            "series": [
                                {"series": {"sourceRange": {"sources": [{"sheetId": lc_ws_id, "startRowIndex": 10, "endRowIndex": 31, "startColumnIndex": 4, "endColumnIndex": 5}]}}, "targetAxis": "BOTTOM_AXIS"}
                            ]
                        }
                    },
                    "position": {
                        "overlayPosition": {
                            "anchorCell": {"sheetId": lc_ws_id, "rowIndex": 3, "columnIndex": 6},
                            "offsetXPixels": 20, "offsetYPixels": 0
                        }
                    }
                }
            }
        })

    if chart_requests:
        try:
            sh.batch_update({"requests": chart_requests})
            print("  ✔️ Đã vẽ biểu đồ động trực tuyến thành công lên Google Sheets.")
        except Exception as e:
            print(f"  ❌ Lỗi vẽ biểu đồ Google Sheets: {e}")

    # Vẽ biểu đồ tĩnh lưu ra Desktop
    print("\n📊 Đang vẽ các biểu đồ OPR & LC cục bộ lưu ra Desktop...")
    try:
        # 1. OPR Chart
        valid_ams = []
        daytime_rates_list = []
        nighttime_rates_list = []
        for am in pivot_df_opr['mapped_AM'].unique():
            row = pivot_df_opr[pivot_df_opr['mapped_AM'] == am].iloc[0]
            if (row['Tong_Don_9h_19h'] + row['Tong_Don_19h_9h']) < 10:
                continue
            daytime_rates_list.append(row['%OPR_9h_19h'])
            nighttime_rates_list.append(row['%OPR_19h_9h'])
            valid_ams.append(am)
            
        x_opr = np.arange(len(valid_ams))
        width_opr = 0.35
        fig, ax = plt.subplots(figsize=(15, 7.5))
        rects1 = ax.bar(x_opr - width_opr/2, [r * 100 for r in daytime_rates_list], width_opr, label='Daytime (9h-19h)', color='#4F46E5', alpha=0.9)
        rects2 = ax.bar(x_opr + width_opr/2, [r * 100 for r in nighttime_rates_list], width_opr, label='Nighttime (19h-9h)', color='#F59E0B', alpha=0.9)
        ax.set_ylabel('Hiệu suất OPR (%)', fontsize=12, fontweight='bold', labelpad=10)
        ax.set_title('HIỆU SUẤT OPR TTS THEO AM VÀ KHUNG GIỜ GIEO (W24)', fontsize=15, fontweight='bold', pad=25, color='#111827')
        ax.set_xticks(x_opr)
        ax.set_xticklabels(valid_ams, rotation=40, ha='right', fontsize=10.5)
        ax.set_ylim(0, 115)
        ax.grid(axis='y', linestyle=':', alpha=0.5, color='#D1D5DB', zorder=0)
        for spine in ['top', 'right', 'left']: ax.spines[spine].set_visible(False)
        ax.spines['bottom'].set_color('#D1D5DB')
        ax.legend(frameon=False, loc='upper right', fontsize=11)
        
        def autolabel_opr(rects, text_color):
            for rect in rects:
                height = rect.get_height()
                if height > 0:
                    ax.annotate(f'{height:.1f}%', xy=(rect.get_x() + rect.get_width() / 2, height), xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=9, fontweight='bold', color=text_color)
        autolabel_opr(rects1, '#3730A3')
        autolabel_opr(rects2, '#92400E')
        fig.tight_layout()
        opr_chart_path = os.path.join(DESKTOP_DIR, "OPR_TTS_theo_AM_va_Khung_Gio.png")
        plt.savefig(opr_chart_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"✔️ Đã lưu biểu đồ OPR TTS tại: {opr_chart_path}")

        # 2. LC Chart
        top_20_sorted = top_20_po.sort_values(by='% rớt LC', ascending=True)
        fig, ax = plt.subplots(figsize=(12, 8.5))
        y_pos = np.arange(len(top_20_sorted))
        bars = ax.barh(y_pos, [r * 100 for r in top_20_sorted['% rớt LC']], align='center', color='#F43F5E', alpha=0.9, height=0.6)
        ax.set_yticks(y_pos)
        ax.set_yticklabels(top_20_sorted['Chi tiết'], fontsize=10, fontweight='medium')
        ax.set_xlabel('Tỷ lệ rớt LC (%)', fontsize=12, fontweight='bold', labelpad=10)
        ax.set_title('TOP 20 BƯU CỤC CÓ TỶ LỆ RỚT LC CAO NHẤT (W24)', fontsize=15, fontweight='bold', pad=25, color='#111827')
        max_val = max(top_20_sorted['% rớt LC'] * 100)
        ax.set_xlim(0, max(max_val * 1.15, 10))
        ax.grid(axis='x', linestyle=':', alpha=0.5, color='#D1D5DB', zorder=0)
        for spine in ['top', 'right', 'bottom']: ax.spines[spine].set_visible(False)
        ax.spines['left'].set_color('#D1D5DB')
        for bar in bars:
            width_val = bar.get_width()
            if width_val > 0:
                ax.annotate(f'{width_val:.2f}%', xy=(width_val, bar.get_y() + bar.get_height() / 2), xytext=(5, 0), textcoords="offset points", ha='left', va='center', fontsize=9.5, fontweight='bold', color='#9F1239')
        fig.tight_layout()
        lc_chart_path = os.path.join(DESKTOP_DIR, "Top_20_Buu_Cuc_Rot_LC.png")
        plt.savefig(lc_chart_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"✔️ Đã lưu biểu đồ Top 20 Bưu cục rớt LC tại: {lc_chart_path}")
    except Exception as chart_err:
        print(f"❌ Lỗi vẽ biểu đồ tĩnh cục bộ OPR/LC: {chart_err}")


# =========================================================================
# PHẦN 3: CHẠY PHÂN TÍCH AM-TỈNH & PHÂN TÍCH AM W24 vs W23 (ĐỒNG BỘ GOOGLE SHEETS)
# =========================================================================
print("\n📊 Đang bắt đầu phần 3: Tính toán Phân tích AM-Tỉnh và Phân tích AM W24 vs W23...")
try:
    import subprocess
    script_path = r'c:\Users\lap4all\Desktop\New folder\sync_online_direct.py'
    if os.path.exists(script_path):
        result = subprocess.run([sys.executable, script_path], cwd=r'c:\Users\lap4all\Desktop\New folder', capture_output=True, text=True, encoding='utf-8')
        print(result.stdout)
        if result.stderr:
            print(f"⚠️ Cảnh báo từ phần 3:\n{result.stderr}")
    else:
        print(f"❌ Lỗi: Không tìm thấy file script {script_path} để chạy Phần 3.")
except Exception as se:
    print(f"❌ Lỗi khi thực hiện chạy Phần 3: {se}")


print("\n🎉 HOÀN THÀNH TẠO TOÀN BỘ BÁO CÁO & DASHBOARD THÀNH CÔNG!")
print("="*60)
