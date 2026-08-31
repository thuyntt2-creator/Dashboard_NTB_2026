import pandas as pd
import urllib.request
import io
import os
import unicodedata

def clean_name(val):
    if pd.isna(val):
        return ""
    val_str = str(val).strip()
    val_str = unicodedata.normalize('NFC', val_str)
    words = val_str.split()
    cleaned = " ".join(w.capitalize() for w in words)
    cleaned = cleaned.replace("HIn", "Hin")
    cleaned = cleaned.replace("Nguyn", "Nguyễn")
    cleaned = cleaned.replace("Trn", "Trần")
    cleaned = cleaned.replace("Trm", "Trầm")
    cleaned = cleaned.replace("Thi", "Thái")
    cleaned = cleaned.replace("Phm", "Phạm")
    cleaned = cleaned.replace("Thnh", "Thành")
    cleaned = cleaned.replace("Cng", "Công")
    cleaned = cleaned.replace("Ngc", "Ngọc")
    cleaned = cleaned.replace("Dim", "Diễm")
    cleaned = cleaned.replace("BiCh", "Bích")
    return cleaned

def sync_online_co_cau():
    # URL for downloading GID 218211549 (CoCauVung) directly as CSV
    url = 'https://docs.google.com/spreadsheets/d/1JZ1eRerRqrpwjZ4HBevQunjd8VquM_cvPFz12TaJfMQ/export?format=csv&gid=218211549'
    print(f"Downloading live CoCauVung sheet from: {url}")
    
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=30) as resp:
            content = resp.read().decode('utf-8')
            
        df = pd.read_csv(io.StringIO(content))
        
        # Clean the column values
        df['Bưu cục'] = df['Bưu cục'].astype(str).str.strip().apply(lambda x: unicodedata.normalize('NFC', x))
        df['Tỉnh'] = df['Tỉnh'].astype(str).str.strip().apply(lambda x: unicodedata.normalize('NFC', x))
        df['Tỉnh'] = df['Tỉnh'].replace({
            'Khánh Hoà': 'Khánh Hòa',
            'Bình Phước': 'Lâm Đồng'
        })
        df['AM'] = df['AM'].apply(clean_name)
        
        # 1. Save co_cau_ntb.csv with Vietnamese headers (Bưu cục, Tỉnh)
        df_ntb = pd.DataFrame()
        df_ntb['warehouse_id'] = df['warehouse_id']
        df_ntb['Bưu cục'] = df['Bưu cục']
        df_ntb['Tỉnh'] = df['Tỉnh']
        df_ntb['AM'] = df['AM']
        df_ntb = df_ntb.dropna(subset=['warehouse_id', 'AM'])
        df_ntb = df_ntb[df_ntb['AM'] != ""]
        df_ntb.to_csv('co_cau_ntb.csv', index=False, encoding='utf-8-sig')
        print("Updated co_cau_ntb.csv with online data (Vietnamese headers)")

        # 2. Save ops_co_cau.csv with ASCII headers (Bu cc, Tnh)
        df_ops = pd.DataFrame()
        df_ops['warehouse_id'] = df['warehouse_id']
        df_ops['Bu cc'] = df['Bưu cục']
        df_ops['BC'] = df_ops['Bu cc']
        df_ops['Tnh'] = df['Tỉnh']
        df_ops['AM'] = df['AM']
        df_ops = df_ops.dropna(subset=['warehouse_id', 'AM'])
        df_ops = df_ops[df_ops['AM'] != ""]
        df_ops.to_csv('ops_co_cau.csv', index=False, encoding='utf-8-sig')
        print("Updated ops_co_cau.csv with online data (ASCII headers)")
        
        unique_ams = sorted(df_ntb['AM'].unique())
        print(f"Sync complete. Count: {len(unique_ams)} AMs")
        
    except Exception as e:
        print(f"Error syncing online CoCauVung: {e}")

if __name__ == "__main__":
    sync_online_co_cau()
