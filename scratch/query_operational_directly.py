import sys
import os

# Configure stdout/stderr to use UTF-8
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Add workspace root to python path to import app.py
sys.path.append(os.getcwd())

import app
import pandas as pd

# Load dataframes like app.py does
df_gtc = pd.read_csv('ops_gtc.csv')
df_ltc = pd.read_csv('ops_ltc.csv')
df_tts = pd.read_csv('ops_tts.csv')

df_gtc = app.clean_ops_df(df_gtc, "gtc")
df_ltc = app.clean_ops_df(df_ltc, "ltc")
df_tts = app.clean_ops_df(df_tts, "tts")

df_gtc = df_gtc[df_gtc['Cấp Quản Lý'] != 'Grand Total'].dropna(subset=["Volume"]).copy()
df_gtc['Leadtime'] = pd.to_numeric(df_gtc['Leadtime'], errors='coerce')

df_ltc = df_ltc[df_ltc['Cấp quản lý'] != 'Grand Total'].dropna(subset=["Volume"]).copy()
df_ltc['Leadtime'] = pd.to_numeric(df_ltc['Leadtime'], errors='coerce')

df_tts = df_tts.dropna(subset=["Volume"]).copy()

print("Calculating operational report for 2026-06-12...")
ops_12 = app.process_operational_report(
    df_gtc=df_gtc,
    df_ltc=df_ltc,
    df_tts=df_tts,
    date="2026-06-12 - Thứ 6"
)
print("  overall_odr_tts:", ops_12.get("overall_odr_tts"))
print("  trend_odr length:", len(ops_12.get("trend_odr", [])))

print("\nCalculating operational report for 2026-06-13...")
ops_13 = app.process_operational_report(
    df_gtc=df_gtc,
    df_ltc=df_ltc,
    df_tts=df_tts,
    date="2026-06-13 - Thứ 7"
)
print("  overall_odr_tts:", ops_13.get("overall_odr_tts"))
print("  trend_odr length:", len(ops_13.get("trend_odr", [])))
