import pandas as pd
import unicodedata
import os

def clean_name(val):
    if pd.isna(val):
        return ""
    val_str = str(val).strip()
    val_str = unicodedata.normalize('NFC', val_str)
    words = val_str.split()
    cleaned = " ".join(w.capitalize() for w in words)
    cleaned = cleaned.replace("HIn", "Hin")
    return cleaned

def sync_co_cau():
    xlsx_path = "co_cau_ntb.xlsx"
    if not os.path.exists(xlsx_path):
        print(f"Error: {xlsx_path} not found.")
        return
        
    df = pd.read_excel(xlsx_path)
    
    # 1. Build co_cau_ntb.csv with Vietnamese headers (Bưu cục, Tỉnh)
    df_ntb = pd.DataFrame()
    df_ntb['warehouse_id'] = df['warehouse_id']
    df_ntb['Bưu cục'] = df['Bưu cục'].astype(str).str.strip().apply(lambda x: unicodedata.normalize('NFC', x))
    df_ntb['Tỉnh'] = df['Tỉnh'].astype(str).str.strip().apply(lambda x: unicodedata.normalize('NFC', x))
    df_ntb['Tỉnh'] = df_ntb['Tỉnh'].replace({
        'Khánh Hoà': 'Khánh Hòa',
        'Bình Phước': 'Lâm Đồng'
    })
    df_ntb['AM'] = df['AM'].apply(clean_name)
    df_ntb = df_ntb.dropna(subset=['warehouse_id', 'AM'])
    df_ntb = df_ntb[df_ntb['AM'] != ""]
    
    df_ntb.to_csv('co_cau_ntb.csv', index=False, encoding='utf-8-sig')
    print("Saved co_cau_ntb.csv with Bưu cục & Tỉnh headers")

    # 2. Build ops_co_cau.csv with ASCII headers (Bu cc, Tnh)
    df_ops = pd.DataFrame()
    df_ops['warehouse_id'] = df['warehouse_id']
    df_ops['Bu cc'] = df['Bưu cục'].astype(str).str.strip().apply(lambda x: unicodedata.normalize('NFC', x))
    df_ops['BC'] = df_ops['Bu cc']
    df_ops['Tnh'] = df['Tỉnh'].astype(str).str.strip().apply(lambda x: unicodedata.normalize('NFC', x))
    df_ops['Tnh'] = df_ops['Tnh'].replace({
        'Khánh Hoà': 'Khánh Hòa',
        'Bình Phước': 'Lâm Đồng'
    })
    df_ops['AM'] = df['AM'].apply(clean_name)
    df_ops = df_ops.dropna(subset=['warehouse_id', 'AM'])
    df_ops = df_ops[df_ops['AM'] != ""]
    
    df_ops.to_csv('ops_co_cau.csv', index=False, encoding='utf-8-sig')
    print("Saved ops_co_cau.csv with Bu cc & Tnh headers")
    
    print("Unique AM Count:", len(df_ntb['AM'].unique()))

if __name__ == "__main__":
    sync_co_cau()
