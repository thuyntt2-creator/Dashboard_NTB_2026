import pandas as pd
import numpy as np
import os
import unicodedata
import matplotlib.pyplot as plt

workspace_dir = r"c:\Users\lap4all\Desktop\New folder"
user_file = os.path.join(workspace_dir, "downloaded_user_sheet.xlsx")

df_gtc_full = pd.read_excel(user_file, sheet_name='dataGTC gốc full hàng')
df_gtc_tts = pd.read_excel(user_file, sheet_name='dataGTC gốc TTS')
df_ltc_full = pd.read_excel(user_file, sheet_name='dataLTC full hàng')
df_ltc_tts = pd.read_excel(user_file, sheet_name='dataLTC TTS')
df_odr_full = pd.read_excel(user_file, sheet_name='dataODRfull hàng ')
df_odr_tts = pd.read_excel(user_file, sheet_name='dataODR TTS')
df_cocau = pd.read_excel(user_file, sheet_name='cocau')

def normalize_name(name):
    if pd.isna(name): return ""
    return unicodedata.normalize('NFC', str(name).strip()).upper()

df_cocau['BC_norm'] = df_cocau['BC'].apply(normalize_name)
bc_to_am = dict(zip(df_cocau['BC_norm'], df_cocau['Am']))

def map_am(bc_name):
    return bc_to_am.get(normalize_name(bc_name), None)

for df in [df_gtc_full, df_gtc_tts, df_ltc_full, df_ltc_tts, df_odr_full, df_odr_tts]:
    if 'Chi tiết' in df.columns:
        df['AM_mapped'] = df['Chi tiết'].apply(map_am)

# Clean numeric columns
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
am_ltc_grouped = df_ltc_w24.groupby('AM_mapped').agg(v=('Vol_Gan', 'sum'), vl=('Vol_LTC', 'sum')).reset_index()
am_ltc_grouped['% LTC'] = (am_ltc_grouped['vl'] / am_ltc_grouped['v']).fillna(0)

# 4. ODR rate by AM
df_odr_w24 = df_odr_full[(df_odr_full['Time'] == week_key) & (~df_odr_full['Quản lý'].astype(str).str.contains('Grand Total|Tổng cộng', case=False, na=False))].copy()
df_odr_w24['Vol_Ontime'] = df_odr_w24['GTC'] * df_odr_w24['%Ontime']
am_odr_grouped = df_odr_w24.groupby('AM_mapped').agg(v=('GTC', 'sum'), vo=('Vol_Ontime', 'sum')).reset_index()
am_odr_grouped['% ODR'] = (am_odr_grouped['vo'] / am_odr_grouped['v']).fillna(0)

all_ams = df_cocau['Am'].dropna().unique()
metrics_df = pd.DataFrame({'AM': all_ams})
metrics_df = metrics_df.merge(am_vol, left_on='AM', right_on='AM_mapped', how='left').drop(columns='AM_mapped').rename(columns={'Volume': 'Volume_W24'}).fillna(0)
metrics_df = metrics_df.merge(am_gtc_grouped[['AM_mapped', '% GTC']], left_on='AM', right_on='AM_mapped', how='left').drop(columns='AM_mapped').rename(columns={'% GTC': 'GTC_W24'}).fillna(0)
metrics_df = metrics_df.merge(am_ltc_grouped[['AM_mapped', '% LTC']], left_on='AM', right_on='AM_mapped', how='left').drop(columns='AM_mapped').rename(columns={'% LTC': 'LTC_W24'}).fillna(0)
metrics_df = metrics_df.merge(am_odr_grouped[['AM_mapped', '% ODR']], left_on='AM', right_on='AM_mapped', how='left').drop(columns='AM_mapped').rename(columns={'% ODR': 'ODR_W24'}).fillna(0)

metrics_df = metrics_df[metrics_df['Volume_W24'] > 0].copy()

# Setup matplotlib
plt.style.use('default')
plt.rcParams['figure.facecolor'] = '#FFFFFF'
plt.rcParams['axes.facecolor'] = '#FFFFFF'
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Segoe UI', 'Roboto', 'Arial', 'sans-serif']
plt.rcParams['text.color'] = '#1E293B'
plt.rcParams['axes.labelcolor'] = '#64748B'
plt.rcParams['xtick.color'] = '#64748B'
plt.rcParams['ytick.color'] = '#64748B'

fig, axs = plt.subplots(2, 2, figsize=(20, 15))

# 1. Volume
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

# 2. GTC
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

# 3. LTC
df_ltc_sorted = metrics_df.sort_values(by='LTC_W24', ascending=False)
ax = axs[1, 0]
rects = ax.bar(df_ltc_sorted['AM'], df_ltc_sorted['LTC_W24'] * 100, color='#06B6D4', alpha=0.9, width=0.6)
ax.set_title("TỶ LỆ LẤY THÀNH CÔNG (LTC) THEO AM (W24)", fontsize=13, fontweight='bold', pad=15)
ax.set_ylabel("Tỷ lệ LTC (%)", fontsize=10, fontweight='bold')
ax.set_xticks(range(len(df_ltc_sorted)))
ax.set_xticklabels(df_ltc_sorted['AM'], rotation=40, ha='right', fontsize=9.5)
ax.set_ylim(0, 110)
ax.grid(axis='y', linestyle=':', alpha=0.5, color='#CBD5E1')
avg_ltc = (df_ltc_w24['Vol_LTC'].sum() / df_ltc_w24['Vol_Gan'].sum()) * 100
ax.axhline(avg_ltc, color='#EF4444', linestyle='--', linewidth=1.5, label=f'Bình quân vùng ({avg_ltc:.1f}%)')
ax.legend(frameon=False, loc='upper right', fontsize=9.5)
for spine in ['top', 'right', 'left']:
    ax.spines[spine].set_visible(False)
ax.spines['bottom'].set_color('#CBD5E1')
for rect in rects:
    h = rect.get_height()
    ax.annotate(f'{h:.1f}%', xy=(rect.get_x() + rect.get_width() / 2, h), xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=8, fontweight='bold', color='#075985')

# 4. ODR
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

out_path = os.path.join(workspace_dir, "scratch", "So_sanh_hieu_suat_cac_AM_W24.png")
plt.savefig(out_path, dpi=200, facecolor='#FFFFFF')
plt.close()
print("Saved consolidated chart successfully to:", out_path)
