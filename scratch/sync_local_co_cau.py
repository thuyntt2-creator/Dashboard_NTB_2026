import pandas as pd
import unicodedata
import os

def clean_name(val):
    if pd.isna(val):
        return ""
    val_str = str(val).strip()
    # Normalize unicode to NFC (standard for Vietnamese)
    val_str = unicodedata.normalize('NFC', val_str)
    # Correct capitalization
    words = val_str.split()
    cleaned = " ".join(w.capitalize() for w in words)
    # Fix specific names if needed
    cleaned = cleaned.replace("HIn", "Hin")
    return cleaned

def sync_co_cau():
    xlsx_path = "co_cau_ntb.xlsx"
    if not os.path.exists(xlsx_path):
        print(f"Error: {xlsx_path} not found.")
        return
        
    df = pd.read_excel(xlsx_path)
    
    # Map raw headers
    df_mapped = pd.DataFrame()
    df_mapped['warehouse_id'] = df['warehouse_id']
    df_mapped['Bu cc'] = df['Bưu cục'].astype(str).str.strip().apply(lambda x: unicodedata.normalize('NFC', x))
    df_mapped['BC'] = df_mapped['Bu cc']
    
    # Normalize Tinh column
    df_mapped['Tnh'] = df['Tỉnh'].astype(str).str.strip().apply(lambda x: unicodedata.normalize('NFC', x))
    df_mapped['Tnh'] = df_mapped['Tnh'].replace({
        'Khánh Hoà': 'Khánh Hòa',
        'Bình Phước': 'Lâm Đồng'
    })
    
    # Normalize AM names
    df_mapped['AM'] = df['AM'].apply(clean_name)
    
    # Filter out empty or header-like rows if any
    df_mapped = df_mapped.dropna(subset=['warehouse_id', 'AM'])
    df_mapped = df_mapped[df_mapped['AM'] != ""]
    
    # Save to both target CSV files
    for target in ['co_cau_ntb.csv', 'ops_co_cau.csv']:
        df_mapped.to_csv(target, index=False, encoding='utf-8-sig')
        print(f"Saved cleaned structure to {target}")
        
    # Print statistics
    unique_ams = sorted(df_mapped['AM'].unique())
    print(f"Total Unique AMs: {len(unique_ams)}")
    print("Unique AM List:")
    for idx, am in enumerate(unique_ams):
        print(f"{idx+1}. {am}")

if __name__ == "__main__":
    sync_co_cau()
