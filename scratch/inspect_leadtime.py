import pandas as pd
import os
import sys

# Set encoding to utf-8 for safety
sys.stdout.reconfigure(encoding='utf-8')

out_path = "scratch/inspect_leadtime_res.txt"

with open(out_path, "w", encoding="utf-8") as f:
    f.write("--- Checking ops_gtc.csv ---\n")
    df_gtc = pd.read_csv("ops_gtc.csv")
    f.write(f"Columns of ops_gtc: {df_gtc.columns.tolist()}\n")
    df_gtc_13 = df_gtc[df_gtc["Time"] == "2026-06-13 - Thứ 7"]
    f.write("Sample ops_gtc data row:\n")
    f.write(df_gtc_13.head(2).to_string() + "\n")

    f.write("\n--- Checking ops_tts.csv ---\n")
    df_tts = pd.read_csv("ops_tts.csv")
    f.write(f"Columns of ops_tts: {df_tts.columns.tolist()}\n")
    df_tts_13 = df_tts[df_tts["Time"] == "2026-06-13 - Thứ 7"]
    f.write("Sample ops_tts data row:\n")
    f.write(df_tts_13.head(2).to_string() + "\n")

    # Search for "Thôn Phúc Hưng" in ops_gtc_13 or ops_tts_13
    phuc_hung = df_gtc_13[df_gtc_13["Chi tiết"].str.contains("Phúc Hưng", na=False, case=False)]
    if not phuc_hung.empty:
        f.write("\nPhúc Hưng in ops_gtc_13:\n")
        f.write(phuc_hung.to_string() + "\n")

    phuc_hung_tts = df_tts_13[df_tts_13["Chi tiết"].str.contains("Phúc Hưng", na=False, case=False)]
    if not phuc_hung_tts.empty:
        f.write("\nPhúc Hưng in ops_tts_13:\n")
        f.write(phuc_hung_tts.to_string() + "\n")

print("Inspection completed!")
