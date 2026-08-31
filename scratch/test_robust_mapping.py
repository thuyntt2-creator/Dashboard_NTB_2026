import pandas as pd
import os
import unicodedata

workspace_dir = r"c:\Users\lap4all\Desktop\New folder"
user_file = os.path.join(workspace_dir, "downloaded_user_sheet.xlsx")
output_file = os.path.join(workspace_dir, "scratch", "test_robust_mapping_res.txt")

def normalize_name(name):
    if pd.isna(name):
        return ""
    # Normalize unicode to NFC, strip, and convert to upper case
    return unicodedata.normalize('NFC', str(name).strip()).upper()

with open(output_file, "w", encoding="utf-8") as f:
    df_opr = pd.read_excel(user_file, sheet_name="OPR TTS")
    df_lc = pd.read_excel(user_file, sheet_name="data rớt LC")
    df_cocau = pd.read_excel(user_file, sheet_name="cocau")
    
    # Pre-process cocau
    df_cocau['Bưu cục_norm'] = df_cocau['Bưu cục'].apply(normalize_name)
    df_cocau['BC_norm'] = df_cocau['BC'].apply(normalize_name)
    
    # Create mapping dictionaries
    bc_to_am = {}
    # First map BC_norm
    for _, r in df_cocau.iterrows():
        bc_to_am[r['BC_norm']] = r['Am']
    # Then map Bưu cục_norm (which might be more complete)
    for _, r in df_cocau.iterrows():
        bc_to_am[r['Bưu cục_norm']] = r['Am']
        
    def get_am(name):
        norm = normalize_name(name)
        if norm in bc_to_am:
            return bc_to_am[norm]
        # Try a fallback of finding if the key is inside or contains
        for k, v in bc_to_am.items():
            if k in norm or norm in k:
                return v
        return None

    # Test OPR TTS
    df_opr['mapped_AM'] = df_opr['kholay'].apply(get_am)
    unmapped_opr = df_opr[df_opr['mapped_AM'].isna()]
    f.write(f"OPR TTS unmatched count: {len(unmapped_opr)}\n")
    if len(unmapped_opr) > 0:
        f.write(f"Unique unmatched OPR kholay:\n{unmapped_opr['kholay'].unique().tolist()}\n\n")
        
    # Test data rớt LC
    df_lc['mapped_AM'] = df_lc['Chi tiết'].apply(get_am)
    unmapped_lc = df_lc[df_lc['mapped_AM'].isna()]
    f.write(f"data rớt LC unmatched count: {len(unmapped_lc)}\n")
    if len(unmapped_lc) > 0:
        f.write(f"Unique unmatched LC Chi tiết:\n{unmapped_lc['Chi tiết'].unique().tolist()}\n")
