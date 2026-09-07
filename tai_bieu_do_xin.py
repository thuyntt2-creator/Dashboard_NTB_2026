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
print(f"Thư mục lưu biểu đồ mặc định: {DESKTOP_DIR}\n")

# Cấu hình Google Sheets
JSON_FILE = r'C:\Users\lap4all\Desktop\Backlog_Automation\credentials.json'
SHEET_ID = '1j6Xm7JRemUGRSfbL-wc8DMwt7qfR7j79w9q79_snVnU'
LOCAL_FILE = r'c:\Users\lap4all\Desktop\New folder\downloaded_user_sheet.xlsx'

# 1. Đọc dữ liệu (Ưu tiên live Google Sheet -> Fallback sang file Excel cục bộ)
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
            df[col] = pd.to_numeric(df[col], errors='coerce')

for df in [df_ltc_full, df_ltc_tts]:
    for col in ['Volume', '%Gán', '%LTC']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

for df in [df_odr_full, df_odr_tts]:
    for col in ['GTC', '%Ontime']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

# 3. Cấu hình Matplotlib Style
plt.style.use('default')
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Segoe UI', 'DejaVu Sans', 'Arial', 'Helvetica']
plt.rcParams['figure.facecolor'] = '#FFFFFF'
plt.rcParams['axes.facecolor'] = '#FFFFFF'
plt.rcParams['text.color'] = '#1F2937'
plt.rcParams['axes.labelcolor'] = '#4B5563'
plt.rcParams['xtick.color'] = '#4B5563'
plt.rcParams['ytick.color'] = '#4B5563'

weeks = ['W21', 'W22', 'W23', 'W24']

# =========================================================================
# BIỂU ĐỒ 1: SẢN LƯỢNG GIAO TỔNG & TTS (Nested Container Bar Chart - SÁNG TẠO)
# =========================================================================
print("📊 Đang vẽ biểu đồ 1: Sản lượng giao lồng ghép (Nested Bars)...")
fig, ax = plt.subplots(figsize=(10, 6))
x = np.arange(len(weeks))

df_gtc_new = df_gtc_full[(df_gtc_full['Loại Hàng'].isin(['Hàng Mới Ca 1', 'Hàng Mới Ca 2'])) & (df_gtc_full['Chi tiết'] != 'Grand Total')]
df_tts_new = df_gtc_tts[(df_gtc_tts['Loại Hàng'].isin(['Hàng Mới Ca 1', 'Hàng Mới Ca 2'])) & (df_gtc_tts['Chi tiết'] != 'Grand Total')]

vols_tot_vals = [
    df_gtc_new[df_gtc_new['Time'] == '2026/21']['Volume'].sum(),
    df_gtc_new[df_gtc_new['Time'] == '2026/22']['Volume'].sum(),
    df_gtc_new[df_gtc_new['Time'] == '2026/23']['Volume'].sum(),
    df_gtc_new[df_gtc_new['Time'] == '2026/24']['Volume'].sum()
]
vols_tts_vals = [
    df_tts_new[df_tts_new['Time'] == '2026/21']['Volume'].sum(),
    df_tts_new[df_tts_new['Time'] == '2026/22']['Volume'].sum(),
    df_tts_new[df_tts_new['Time'] == '2026/23']['Volume'].sum(),
    df_tts_new[df_tts_new['Time'] == '2026/24']['Volume'].sum()
]

# Vẽ cột chứa bên ngoài (Tổng Vùng) - bán trong suốt, viền mỏng nét đứt tạo hiệu ứng container
rects1 = ax.bar(x, vols_tot_vals, width=0.45, label='Tổng vùng NTB', color='#4F46E5', alpha=0.15, edgecolor='#4F46E5', linewidth=1.5, zorder=3)
# Vẽ cột cốt lõi bên trong (Tuyến TTS) - nhỏ hơn và đặc màu
rects2 = ax.bar(x, vols_tts_vals, width=0.22, label='Trong đó: Tuyến TTS', color='#06B6D4', alpha=1.0, edgecolor='none', zorder=3)

ax.set_ylabel('Sản lượng giao (đơn)', fontsize=11, fontweight='bold', labelpad=10)
ax.set_title('SẢN LƯỢNG GIAO TỔNG & TTS VÙNG NTB (W21 - W24)', fontsize=14, fontweight='bold', pad=25, color='#111827')
ax.set_xticks(x)
ax.set_xticklabels(weeks, fontsize=11)
ax.legend(frameon=False, loc='upper left', bbox_to_anchor=(0.02, 0.98), fontsize=10)
ax.grid(axis='y', linestyle=':', alpha=0.6, color='#E5E7EB', zorder=0)

for spine in ['top', 'right', 'left']:
    ax.spines[spine].set_visible(False)
ax.spines['bottom'].set_color('#D1D5DB')

# Ghi nhãn số liệu lên đầu từng bar
for i, rect in enumerate(rects1):
    h = rect.get_height()
    ax.annotate(f'{h:,.0f}', xy=(rect.get_x() + rect.get_width() / 2, h),
                xytext=(-18, 5), textcoords="offset points", ha='center', va='bottom', fontsize=9.5, fontweight='bold', color='#4F46E5')

for i, rect in enumerate(rects2):
    h = rect.get_height()
    ax.annotate(f'{h:,.0f}', xy=(rect.get_x() + rect.get_width() / 2, h),
                xytext=(18, 5), textcoords="offset points", ha='center', va='bottom', fontsize=9.5, fontweight='bold', color='#0891B2')

fig.tight_layout()
path1 = os.path.join(DESKTOP_DIR, "Sản_lượng_giao_tổng_TTS_NTB.png")
plt.savefig(path1, dpi=300, bbox_inches='tight')
plt.close()
print(f"✔️ Đã lưu: {path1}")


# =========================================================================
# BIỂU ĐỒ 2: XU HƯỚNG TỈ LỆ GTC MỚI (Gradient Area Line Chart - SÁNG TẠO)
# =========================================================================
print("📈 Đang vẽ biểu đồ 2: Xu hướng tỉ lệ GTC với vùng bóng đổ (Gradient Area)...")
fig, ax = plt.subplots(figsize=(10, 6))

gtc_tot_rates = []
gtc_tts_rates = []
for week in ['2026/21', '2026/22', '2026/23', '2026/24']:
    sub_tot = df_gtc_full[(df_gtc_full['Loại Hàng'].isin(['Hàng Mới Ca 1', 'Hàng Mới Ca 2'])) & (df_gtc_full['Time'] == week) & (df_gtc_full['Chi tiết'] != 'Grand Total')]
    gtc_tot_rates.append((sub_tot['Volume'] * sub_tot['% GTC']).sum() / sub_tot['Volume'].sum() if not sub_tot.empty else 0)
    
    sub_tts = df_gtc_tts[(df_gtc_tts['Loại Hàng'].isin(['Hàng Mới Ca 1', 'Hàng Mới Ca 2'])) & (df_gtc_tts['Time'] == week) & (df_gtc_tts['Chi tiết'] != 'Grand Total')]
    gtc_tts_rates.append((sub_tts['Volume'] * sub_tts['% GTC']).sum() / sub_tts['Volume'].sum() if not sub_tts.empty else 0)

# Vẽ bóng đổ nhẹ dưới các đường line
ax.fill_between(weeks, [r * 100 for r in gtc_tot_rates], color='#4F46E5', alpha=0.08)
ax.fill_between(weeks, [r * 100 for r in gtc_tts_rates], color='#F43F5E', alpha=0.06)

# Vẽ đường viền chính
ax.plot(weeks, [r * 100 for r in gtc_tot_rates], marker='o', linewidth=3, color='#4F46E5', mfc='white', mew=2.5, ms=8, label='GTC Tổng', zorder=3)
ax.plot(weeks, [r * 100 for r in gtc_tts_rates], marker='o', linewidth=3, color='#F43F5E', mfc='white', mew=2.5, ms=8, label='GTC TTS', zorder=3)

ax.set_ylabel('Tỉ lệ giao thành công (%)', fontsize=11, fontweight='bold', labelpad=10)
ax.set_title('XU HƯỚNG TỈ LỆ GIAO THÀNH CÔNG MỚI (W21 - W24)', fontsize=14, fontweight='bold', pad=25, color='#111827')
ax.set_ylim(40, 85)
ax.legend(frameon=False, loc='lower left', fontsize=10)
ax.grid(axis='y', linestyle=':', alpha=0.6, color='#E5E7EB', zorder=0)

for spine in ['top', 'right', 'left']:
    ax.spines[spine].set_visible(False)
ax.spines['bottom'].set_color('#D1D5DB')

for i, (t, s) in enumerate(zip(gtc_tot_rates, gtc_tts_rates)):
    ax.annotate(f'{t:.2%}', (weeks[i], t*100), textcoords="offset points", xytext=(0, 10), ha='center', fontweight='bold', color='#4F46E5', fontsize=10)
    ax.annotate(f'{s:.2%}', (weeks[i], s*100), textcoords="offset points", xytext=(0, -18), ha='center', fontweight='bold', color='#F43F5E', fontsize=10)

fig.tight_layout()
path2 = os.path.join(DESKTOP_DIR, "Xu_hướng_tỉ_lệ_GTC_mới.png")
plt.savefig(path2, dpi=300, bbox_inches='tight')
plt.close()
print(f"✔️ Đã lưu: {path2}")


# =========================================================================
# BIỂU ĐỒ 3: XU HƯỚNG TỈ LỆ LTC (Modern Step Area Chart - SÁNG TẠO)
# =========================================================================
print("📈 Đang vẽ biểu đồ 3: Xu hướng tỉ lệ LTC dạng đường gấp khúc (Step Chart)...")
fig, ax = plt.subplots(figsize=(10, 6))

ltc_tot_rates = []
ltc_tts_rates = []
for week in ['2026/21', '2026/22', '2026/23', '2026/24']:
    sub_tot = df_ltc_full[(df_ltc_full['Chi tiết'] != 'Grand Total') & (df_ltc_full['Time'] == week)]
    ltc_tot_rates.append((sub_tot['Volume'] * sub_tot['%Gán'] * sub_tot['%LTC']).sum() / (sub_tot['Volume'] * sub_tot['%Gán']).sum() if not sub_tot.empty else 0)
    
    sub_tts = df_ltc_tts[(df_ltc_tts['Chi tiết'] != 'Grand Total') & (df_ltc_tts['Time'] == week)]
    ltc_tts_rates.append((sub_tts['Volume'] * sub_tts['%Gán'] * sub_tts['%LTC']).sum() / (sub_tts['Volume'] * sub_tts['%Gán']).sum() if not sub_tts.empty else 0)

# Vẽ đường Step gập khúc tạo sự sáng tạo, tách biệt với các Line thông thường
ax.step(weeks, [r * 100 for r in ltc_tot_rates], where='mid', color='#10B981', linewidth=3, label='LTC Tổng (Bình quân gia quyền)', zorder=3)
ax.step(weeks, [r * 100 for r in ltc_tts_rates], where='mid', color='#F59E0B', linewidth=3, label='LTC TTS (Bình quân gia quyền)', zorder=3)

# Tô màu vùng bóng đổ gập khúc
ax.fill_between(weeks, [r * 100 for r in ltc_tot_rates], step='mid', color='#10B981', alpha=0.05)
ax.fill_between(weeks, [r * 100 for r in ltc_tts_rates], step='mid', color='#F59E0B', alpha=0.03)

# Điểm marker rời làm nổi bật điểm tuần
ax.scatter(weeks, [r * 100 for r in ltc_tot_rates], color='#10B981', edgecolor='white', linewidth=2, s=80, zorder=4)
ax.scatter(weeks, [r * 100 for r in ltc_tts_rates], color='#F59E0B', edgecolor='white', linewidth=2, s=80, zorder=4)

ax.set_ylabel('Tỉ lệ lấy thành công (%)', fontsize=11, fontweight='bold', labelpad=10)
ax.set_title('XU HƯỚNG TỈ LỆ LẤY THÀNH CÔNG (W21 - W24)', fontsize=14, fontweight='bold', pad=25, color='#111827')
ax.set_ylim(80, 100)
ax.legend(frameon=False, loc='lower left', fontsize=10)
ax.grid(axis='y', linestyle=':', alpha=0.6, color='#E5E7EB', zorder=0)

for spine in ['top', 'right', 'left']:
    ax.spines[spine].set_visible(False)
ax.spines['bottom'].set_color('#D1D5DB')

for i, (t, s) in enumerate(zip(ltc_tot_rates, ltc_tts_rates)):
    ax.annotate(f'{t:.2%}', (weeks[i], t*100), textcoords="offset points", xytext=(0, 10), ha='center', fontweight='bold', color='#10B981', fontsize=10)
    ax.annotate(f'{s:.2%}', (weeks[i], s*100), textcoords="offset points", xytext=(0, -18), ha='center', fontweight='bold', color='#F59E0B', fontsize=10)

fig.tight_layout()
path3 = os.path.join(DESKTOP_DIR, "Xu_hướng_tỉ_lệ_LTC.png")
plt.savefig(path3, dpi=300, bbox_inches='tight')
plt.close()
print(f"✔️ Đã lưu: {path3}")


# =========================================================================
# BIỂU ĐỒ 4: ĐỒNG BỘ DỰ LIỆU ODR TỔNG VS ODR TTS (Side-by-side Dashboard - SÁNG TẠO)
# =========================================================================
print("📈 Đang vẽ biểu đồ 4: Dashboard so sánh song song ODR Tổng vs ODR TTS...")
# Tạo 2 đồ thị nằm ngang cạnh nhau để so sánh trực diện, tránh bị nhầm lẫn
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7), sharey=True)

# 4.1. Chuẩn bị dữ liệu ODR Tổng
df_odr_tot = df_odr_full.copy()
df_odr_tot['Vol_Ontime'] = df_odr_tot['GTC'] * df_odr_tot['%Ontime']
odr_grouped = df_odr_tot.groupby(['Tỉnh_mapped', 'Time']).agg(v=('GTC', 'sum'), vo=('Vol_Ontime', 'sum')).reset_index()
odr_grouped['Pct_ODR'] = odr_grouped['vo'] / odr_grouped['v']

# 4.2. Chuẩn bị dữ liệu ODR TTS
df_odr_tts_tot = df_odr_tts.copy()
# Loại bỏ các dòng tổng cộng
df_odr_tts_tot = df_odr_tts_tot[~df_odr_tts_tot['Quản lý'].astype(str).str.contains('Grand Total|Tổng cộng', case=False, na=False)].copy()
df_odr_tts_tot['Vol_Ontime'] = df_odr_tts_tot['GTC'] * df_odr_tts_tot['%Ontime']
odr_tts_grouped = df_odr_tts_tot.groupby(['Tỉnh_mapped', 'Time']).agg(v=('GTC', 'sum'), vo=('Vol_Ontime', 'sum')).reset_index()
odr_tts_grouped['Pct_ODR'] = odr_tts_grouped['vo'] / odr_tts_grouped['v']

provinces = odr_grouped['Tỉnh_mapped'].dropna().unique()
colors = ['#3B82F6', '#EF4444', '#10B981', '#F59E0B', '#8B5CF6']

# Vẽ Đồ thị bên trái: ODR TỔNG
for idx, prov in enumerate(provinces):
    sub = odr_grouped[odr_grouped['Tỉnh_mapped'] == prov]
    sub = sub.set_index('Time').reindex(['2026/21', '2026/22', '2026/23', '2026/24']).reset_index()
    rates = sub['Pct_ODR'].fillna(0) * 100
    
    ax1.plot(weeks, rates, marker='o', linewidth=2.5, color=colors[idx % len(colors)], mfc='white', mew=2, ms=8, label=prov, zorder=3)
    if not rates.empty:
        val = rates.iloc[-1]
        ax1.annotate(f'{val/100:.1%}', (weeks[-1], val), textcoords="offset points", xytext=(8, -3), ha='left', fontweight='bold', color=colors[idx % len(colors)], fontsize=9.5)

ax1.set_ylabel('Tỉ lệ giao đúng hạn ODR (%)', fontsize=11, fontweight='bold')
ax1.set_title('ODR TỔNG THEO TỈNH VÙNG NTB', fontsize=12, fontweight='bold', pad=15, color='#1F2937')
ax1.set_ylim(80, 100)
ax1.legend(frameon=False, loc='lower left', fontsize=9.5)
ax1.grid(axis='y', linestyle=':', alpha=0.5, color='#E5E7EB')
for spine in ['top', 'right', 'left']:
    ax1.spines[spine].set_visible(False)
ax1.spines['bottom'].set_color('#D1D5DB')

# Vẽ Đồ thị bên phải: ODR TUYẾN TTS (Bổ sung mới)
for idx, prov in enumerate(provinces):
    sub = odr_tts_grouped[odr_tts_grouped['Tỉnh_mapped'] == prov]
    sub = sub.set_index('Time').reindex(['2026/21', '2026/22', '2026/23', '2026/24']).reset_index()
    rates = sub['Pct_ODR'].fillna(0) * 100
    
    # Sử dụng marker hình vuông ('s') để dễ phân biệt
    ax2.plot(weeks, rates, marker='s', linewidth=2.5, color=colors[idx % len(colors)], mfc='white', mew=2, ms=8, label=prov, zorder=3)
    if not rates.empty:
        val = rates.iloc[-1]
        ax2.annotate(f'{val/100:.1%}', (weeks[-1], val), textcoords="offset points", xytext=(8, -3), ha='left', fontweight='bold', color=colors[idx % len(colors)], fontsize=9.5)

ax2.set_title('ODR TUYẾN TTS THEO TỈNH VÙNG NTB (MỚI)', fontsize=12, fontweight='bold', pad=15, color='#1F2937')
ax2.legend(frameon=False, loc='lower left', fontsize=9.5)
ax2.grid(axis='y', linestyle=':', alpha=0.5, color='#E5E7EB')
for spine in ['top', 'right', 'left']:
    ax2.spines[spine].set_visible(False)
ax2.spines['bottom'].set_color('#D1D5DB')

fig.suptitle('XU HƯỚNG ODR TỔNG VS ODR TUYẾN TTS (W21 - W24)', fontsize=15, fontweight='bold', y=0.98, color='#111827')
fig.tight_layout(rect=[0, 0, 1, 0.95])

path4 = os.path.join(DESKTOP_DIR, "Xu_hướng_ODR_theo_tỉnh.png")
plt.savefig(path4, dpi=300, bbox_inches='tight')
plt.close()
print(f"✔️ Đã lưu: {path4}")

print("\n🎉 HOÀN TẤT! Đã thiết kế lại 4 biểu đồ sáng tạo khác biệt và lưu trực tiếp ra Desktop!")
