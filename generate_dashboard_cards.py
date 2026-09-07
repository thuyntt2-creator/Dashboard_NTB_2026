import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# File paths
input_file = r"c:\Users\lap4all\Desktop\New folder\downloaded_user_sheet.xlsx"
output_dir = r"c:\Users\lap4all\Desktop"

print("Loading Data...")
df_gtc_full = pd.read_excel(input_file, sheet_name='dataGTC gốc full hàng')
df_gtc_tts = pd.read_excel(input_file, sheet_name='dataGTC gốc TTS')
df_ltc_full = pd.read_excel(input_file, sheet_name='dataLTC full hàng')
df_ltc_tts = pd.read_excel(input_file, sheet_name='dataLTC TTS')
df_odr_full = pd.read_excel(input_file, sheet_name='dataODRfull hàng ')
df_odr_tts = pd.read_excel(input_file, sheet_name='dataODR TTS')

# Standardize mappings
df_cocau = pd.read_excel(input_file, sheet_name='cocau')
import unicodedata
def normalize_name(name):
    if pd.isna(name): return ""
    return unicodedata.normalize('NFC', str(name).strip()).upper()

df_cocau['BC_norm'] = df_cocau['BC'].apply(normalize_name)
df_cocau['Am_norm'] = df_cocau['Am'].apply(normalize_name)
df_cocau['Tỉnh_norm'] = df_cocau['Tỉnh'].apply(normalize_name)

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

for df in [df_gtc_full, df_gtc_tts, df_ltc_full, df_ltc_tts, df_odr_full, df_odr_tts]:
    if 'Chi tiết' in df.columns:
        df['AM_mapped'] = df['Chi tiết'].apply(map_am)
        df['Tỉnh_mapped'] = df['Chi tiết'].apply(map_tinh)
    if 'Quản lý' in df.columns:
        df['Tỉnh_mapped_ql'] = df['Quản lý'].apply(get_province_from_ql)
        if 'Tỉnh_mapped' in df.columns:
            df['Tỉnh_mapped'] = df['Tỉnh_mapped'].fillna(df['Tỉnh_mapped_ql'])
        else:
            df['Tỉnh_mapped'] = df['Tỉnh_mapped_ql']

weeks = ['W21', 'W22', 'W23', 'W24']
weeks_keys = ['2026/21', '2026/22', '2026/23', '2026/24']

# Configure Dashboard Matplotlib Theme (Dark Theme)
plt.rcParams['figure.facecolor'] = '#0B0F19' # Modern Dark Slate
plt.rcParams['axes.facecolor'] = '#0B0F19'
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Segoe UI', 'Roboto', 'Arial', 'sans-serif']
plt.rcParams['text.color'] = '#F8FAFC' # Slate 50
plt.rcParams['axes.labelcolor'] = '#94A3B8' # Slate 400
plt.rcParams['xtick.color'] = '#94A3B8'
plt.rcParams['ytick.color'] = '#94A3B8'

print("Generating Dashboard Cards...")

# CARD 1: Sản lượng
fig, ax = plt.subplots(figsize=(8, 5.2))
fig.subplots_adjust(top=0.70, left=0.08, right=0.92, bottom=0.12)

df_gtc_new = df_gtc_full[(df_gtc_full['Loại Hàng'].isin(['Hàng Mới Ca 1', 'Hàng Mới Ca 2'])) & (df_gtc_full['Chi tiết'] != 'Grand Total')]
df_tts_new = df_gtc_tts[(df_gtc_tts['Loại Hàng'].isin(['Hàng Mới Ca 1', 'Hàng Mới Ca 2'])) & (df_gtc_tts['Chi tiết'] != 'Grand Total')]

vols_tot = [df_gtc_new[df_gtc_new['Time'] == wk]['Volume'].sum() for wk in weeks_keys]
vols_tts = [df_tts_new[df_tts_new['Time'] == wk]['Volume'].sum() for wk in weeks_keys]

x = np.arange(len(weeks))
ax.plot(x, vols_tot, marker='o', linewidth=3.5, color='#4F46E5', mfc='white', mew=2.5, ms=8, label='Tổng Vùng NTB', zorder=4)
ax.fill_between(x, vols_tot, color='#4F46E5', alpha=0.15)
ax.plot(x, vols_tts, marker='o', linewidth=3.5, color='#06B6D4', mfc='white', mew=2.5, ms=8, label='Trong đó: Tuyến TTS', zorder=4)
ax.fill_between(x, vols_tts, color='#06B6D4', alpha=0.15)

# Text / KPI labels inside the Card (Aligned outside the plot area)
fig.text(0.06, 0.89, "SẢN LƯỢNG GIAO TỔNG & TTS VÙNG NTB", fontsize=10, fontweight='bold', color='#94A3B8')
fig.text(0.06, 0.77, "380,193 đơn", fontsize=24, fontweight='bold', color='#FFFFFF')
fig.text(0.34, 0.78, "▲ +8.03% vs W23", fontsize=9.5, fontweight='bold', color='#10B981', bbox=dict(facecolor='#064E3B', edgecolor='none', boxstyle='round,pad=0.3'))

# Chart styling
ax.set_ylim(0, 430000)
ax.set_xticks(x)
ax.set_xticklabels(weeks, fontsize=10)
ax.grid(axis='y', linestyle=':', alpha=0.2, color='#E2E8F0', zorder=0)
for spine in ['top', 'right', 'left', 'bottom']:
    ax.spines[spine].set_visible(False)
ax.legend(frameon=False, loc='upper left', fontsize=9, labelcolor='#94A3B8')

# Annotations on final point
ax.annotate(f"{vols_tot[-1]:,.0f}", (x[-1], vols_tot[-1]), textcoords="offset points", xytext=(0,12), ha='center', fontweight='bold', color='#4F46E5')
ax.annotate(f"{vols_tts[-1]:,.0f}", (x[-1], vols_tts[-1]), textcoords="offset points", xytext=(0,12), ha='center', fontweight='bold', color='#06B6D4')

plt.savefig(os.path.join(output_dir, "db_card_volume.png"), dpi=200, facecolor='#0B0F19')
plt.close()


# CARD 2: GTC
fig, ax = plt.subplots(figsize=(8, 5.2))
fig.subplots_adjust(top=0.70, left=0.08, right=0.92, bottom=0.12)

gtc_tot_rates = []
gtc_tts_rates = []
for week in weeks_keys:
    sub_tot = df_gtc_full[(df_gtc_full['Loại Hàng'].isin(['Hàng Mới Ca 1', 'Hàng Mới Ca 2'])) & (df_gtc_full['Time'] == week) & (df_gtc_full['Chi tiết'] != 'Grand Total')]
    gtc_tot_rates.append((sub_tot['Volume'] * sub_tot['% GTC']).sum() / sub_tot['Volume'].sum() if not sub_tot.empty else 0)
    sub_tts = df_gtc_tts[(df_gtc_tts['Loại Hàng'].isin(['Hàng Mới Ca 1', 'Hàng Mới Ca 2'])) & (df_gtc_tts['Time'] == week) & (df_gtc_tts['Chi tiết'] != 'Grand Total')]
    gtc_tts_rates.append((sub_tts['Volume'] * sub_tts['% GTC']).sum() / sub_tts['Volume'].sum() if not sub_tts.empty else 0)

ax.plot(x, [r * 100 for r in gtc_tot_rates], marker='o', linewidth=3.5, color='#4F46E5', mfc='white', mew=2.5, ms=8, label='GTC Tổng', zorder=4)
ax.fill_between(x, [r * 100 for r in gtc_tot_rates], color='#4F46E5', alpha=0.1)
ax.plot(x, [r * 100 for r in gtc_tts_rates], marker='o', linewidth=3.5, color='#F43F5E', mfc='white', mew=2.5, ms=8, label='GTC TTS', zorder=4)
ax.fill_between(x, [r * 100 for r in gtc_tts_rates], color='#F43F5E', alpha=0.1)

fig.text(0.06, 0.89, "TỈ LỆ GIAO THÀNH CÔNG MỚI (GTC)", fontsize=10, fontweight='bold', color='#94A3B8')
fig.text(0.06, 0.77, f"{gtc_tot_rates[-1]:.2%}", fontsize=24, fontweight='bold', color='#FFFFFF')
fig.text(0.24, 0.78, "▲ +0.24% vs W23", fontsize=9.5, fontweight='bold', color='#10B981', bbox=dict(facecolor='#064E3B', edgecolor='none', boxstyle='round,pad=0.3'))

ax.set_ylim(40, 85)
ax.set_xticks(x)
ax.set_xticklabels(weeks, fontsize=10)
ax.grid(axis='y', linestyle=':', alpha=0.2, color='#E2E8F0', zorder=0)
for spine in ['top', 'right', 'left', 'bottom']:
    ax.spines[spine].set_visible(False)
ax.legend(frameon=False, loc='lower right', fontsize=9, labelcolor='#94A3B8')

for i, (t, s) in enumerate(zip(gtc_tot_rates, gtc_tts_rates)):
    ax.annotate(f'{t:.2%}', (x[i], t*100), textcoords="offset points", xytext=(0, 12), ha='center', fontweight='semibold', color='#4F46E5', fontsize=9)
    ax.annotate(f'{s:.2%}', (x[i], s*100), textcoords="offset points", xytext=(0, -20), ha='center', fontweight='semibold', color='#F43F5E', fontsize=9)

plt.savefig(os.path.join(output_dir, "db_card_gtc.png"), dpi=200, facecolor='#0B0F19')
plt.close()


# CARD 3: LTC
fig, ax = plt.subplots(figsize=(8, 5.2))
fig.subplots_adjust(top=0.70, left=0.08, right=0.92, bottom=0.12)

ltc_tot_rates = []
ltc_tts_rates = []
for week in weeks_keys:
    sub_tot = df_ltc_full[(df_ltc_full['Chi tiết'] != 'Grand Total') & (df_ltc_full['Time'] == week)]
    ltc_tot_rates.append((sub_tot['Volume'] * sub_tot['%Gán'] * sub_tot['%LTC']).sum() / (sub_tot['Volume'] * sub_tot['%Gán']).sum() if not sub_tot.empty else 0)
    sub_tts = df_ltc_tts[(df_ltc_tts['Chi tiết'] != 'Grand Total') & (df_ltc_tts['Time'] == week)]
    ltc_tts_rates.append((sub_tts['Volume'] * sub_tts['%Gán'] * sub_tts['%LTC']).sum() / (sub_tts['Volume'] * sub_tts['%Gán']).sum() if not sub_tts.empty else 0)

ax.plot(x, [r * 100 for r in ltc_tot_rates], marker='o', linewidth=3.5, color='#10B981', mfc='white', mew=2.5, ms=8, label='LTC Tổng (Bình quân gia quyền)', zorder=4)
ax.fill_between(x, [r * 100 for r in ltc_tot_rates], color='#10B981', alpha=0.1)
ax.plot(x, [r * 100 for r in ltc_tts_rates], marker='o', linewidth=3.5, color='#F59E0B', mfc='white', mew=2.5, ms=8, label='LTC TTS (Bình quân gia quyền)', zorder=4)
ax.fill_between(x, [r * 100 for r in ltc_tts_rates], color='#F59E0B', alpha=0.1)

fig.text(0.06, 0.89, "TỈ LỆ LẤY THÀNH CÔNG (LTC)", fontsize=10, fontweight='bold', color='#94A3B8')
fig.text(0.06, 0.77, f"{ltc_tot_rates[-1]:.2%}", fontsize=24, fontweight='bold', color='#FFFFFF')
fig.text(0.24, 0.78, "▼ -0.27% vs W23", fontsize=9.5, fontweight='bold', color='#EF4444', bbox=dict(facecolor='#7F1D1D', edgecolor='none', boxstyle='round,pad=0.3'))

ax.set_ylim(80, 100)
ax.set_xticks(x)
ax.set_xticklabels(weeks, fontsize=10)
ax.grid(axis='y', linestyle=':', alpha=0.2, color='#E2E8F0', zorder=0)
for spine in ['top', 'right', 'left', 'bottom']:
    ax.spines[spine].set_visible(False)
ax.legend(frameon=False, loc='lower right', fontsize=9, labelcolor='#94A3B8')

for i, (t, s) in enumerate(zip(ltc_tot_rates, ltc_tts_rates)):
    ax.annotate(f'{t:.2%}', (x[i], t*100), textcoords="offset points", xytext=(0, 12), ha='center', fontweight='semibold', color='#10B981', fontsize=9)
    ax.annotate(f'{s:.2%}', (x[i], s*100), textcoords="offset points", xytext=(0, -20), ha='center', fontweight='semibold', color='#F59E0B', fontsize=9)

plt.savefig(os.path.join(output_dir, "db_card_ltc.png"), dpi=200, facecolor='#0B0F19')
plt.close()


# CARD 4: ODR by Province
fig, ax = plt.subplots(figsize=(8, 5.2))
fig.subplots_adjust(top=0.72, left=0.08, right=0.92, bottom=0.12)

df_odr_tot = df_odr_full.copy()
df_odr_tot['Vol_Ontime'] = df_odr_tot['GTC'] * df_odr_tot['%Ontime']
odr_grouped = df_odr_tot.groupby(['Tỉnh_mapped', 'Time']).agg(
    v=('GTC', 'sum'), vo=('Vol_Ontime', 'sum')
).reset_index()
odr_grouped['Pct_ODR'] = odr_grouped['vo'] / odr_grouped['v']

provinces = odr_grouped['Tỉnh_mapped'].dropna().unique()
colors = ['#3B82F6', '#EF4444', '#10B981', '#F59E0B', '#8B5CF6']

for idx, prov in enumerate(provinces):
    sub = odr_grouped[odr_grouped['Tỉnh_mapped'] == prov]
    sub = sub.set_index('Time').reindex(weeks_keys).reset_index()
    rates = sub['Pct_ODR'].fillna(0) * 100
    ax.plot(x, rates, marker='o', linewidth=2.5, color=colors[idx % len(colors)], mfc='white', mew=2, ms=7, label=prov)
    if not rates.empty:
        val = rates.iloc[-1]
        ax.annotate(f'{val/100:.1%}', (x[-1], val), textcoords="offset points", xytext=(10, -3), ha='left', fontweight='semibold', color=colors[idx % len(colors)], fontsize=9)

fig.text(0.06, 0.89, "TỈ LỆ GIAO ĐÚNG HẠN ODR THEO TỈNH", fontsize=10, fontweight='bold', color='#94A3B8')

# Calculate region average ODR for W24
df_odr_w24 = df_odr_full[df_odr_full['Time'] == '2026/24']
df_odr_w23 = df_odr_full[df_odr_full['Time'] == '2026/23']
odr_w24_avg = (df_odr_w24['GTC'] * df_odr_w24['%Ontime']).sum() / df_odr_w24['GTC'].sum()
odr_w23_avg = (df_odr_w23['GTC'] * df_odr_w23['%Ontime']).sum() / df_odr_w23['GTC'].sum()
diff_odr = odr_w24_avg - odr_w23_avg

fig.text(0.06, 0.77, f"{odr_w24_avg:.2%}", fontsize=24, fontweight='bold', color='#FFFFFF')
fig.text(0.24, 0.78, f"{'▲' if diff_odr >= 0 else '▼'} {diff_odr:+.2%} vs W23", fontsize=9.5, fontweight='bold', color='#10B981' if diff_odr >= 0 else '#EF4444', bbox=dict(facecolor='#064E3B' if diff_odr >= 0 else '#7F1D1D', edgecolor='none', boxstyle='round,pad=0.3'))

ax.set_ylim(80, 100)
ax.set_xticks(x)
ax.set_xticklabels(weeks, fontsize=10)
ax.grid(axis='y', linestyle=':', alpha=0.2, color='#E2E8F0', zorder=0)
for spine in ['top', 'right', 'left', 'bottom']:
    ax.spines[spine].set_visible(False)
ax.legend(frameon=False, loc='lower left', fontsize=9, labelcolor='#94A3B8')

plt.savefig(os.path.join(output_dir, "db_card_odr.png"), dpi=200, facecolor='#0B0F19')
plt.close()

print("All dark theme dashboard cards generated successfully!")
