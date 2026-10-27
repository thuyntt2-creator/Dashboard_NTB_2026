import sys, os
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')
import gspread
import pandas as pd
from google.oauth2.credentials import Credentials as UserCredentials

SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
creds = UserCredentials.from_authorized_user_file('authorized_user.json', scopes=SCOPES)
gc = gspread.authorize(creds)
sheet_id = '1ll3CaTcBj-tp8kcamMUftBLb9OriIoIHFhIyL3LYzvo'
sh = gc.open_by_key(sheet_id)

def analyze_sheet(title):
    ws = sh.worksheet(title)
    data = ws.get_all_values()
    if not data or len(data) <= 1:
        print(f"Sheet {title} is empty or header only.")
        return None
    headers = [h.strip() for h in data[0]]
    cols = []
    for i, h in enumerate(headers):
        cols.append(h if h else f"col_{i}")
    df = pd.DataFrame(data[1:], columns=cols)
    df = df[df.apply(lambda r: any(r.str.strip()), axis=1)]
    print("=" * 60)
    print(f"=== BÁO CÁO SHEET: {title} (Tổng số đơn: {len(df)}) ===")
    print("=" * 60)
    
    if 'Tiền COD' in df.columns:
        cod_clean = df['Tiền COD'].astype(str).str.replace(',', '', regex=False).str.replace('.', '', regex=False).str.strip()
        df['COD_num'] = pd.to_numeric(cod_clean, errors='coerce').fillna(0)
        total_cod = df['COD_num'].sum()
        mean_cod = df['COD_num'].mean()
        print(f"Tổng tiền COD: {total_cod:,.0f} đ | Trung bình: {mean_cod:,.0f} đ/đơn")
        if 'Bucket COD' in df.columns:
            print("\n-- Theo khoảng COD (Bucket COD):")
            print(df['Bucket COD'].value_counts().to_string())
            
    print("\n-- Theo Tỉnh giao:")
    if 'Tỉnh giao' in df.columns:
        print(df['Tỉnh giao'].value_counts().to_string())
        
    print("\n-- Theo AM:")
    if 'AM' in df.columns:
        am_stats = df.groupby('AM').size().reset_index(name='Số đơn')
        if 'COD_num' in df.columns:
            am_cod = df.groupby('AM')['COD_num'].sum().reset_index(name='Tổng COD')
            am_stats = am_stats.merge(am_cod, on='AM')
            am_stats['Tổng COD'] = am_stats['Tổng COD'].apply(lambda x: f"{x:,.0f} đ")
        print(am_stats.sort_values(by='Số đơn', ascending=False).to_string(index=False))
        
    print("\n-- Theo Bưu cục (Kho hiện tại):")
    kho_col = 'Kho hiện tại' if 'Kho hiện tại' in df.columns else 'Kho giao'
    if kho_col in df.columns:
        kho_stats = df.groupby(kho_col).size().reset_index(name='Số đơn')
        if 'COD_num' in df.columns:
            kho_cod = df.groupby(kho_col)['COD_num'].sum().reset_index(name='Tổng COD')
            kho_stats = kho_stats.merge(kho_cod, on=kho_col)
            kho_stats['Tổng COD'] = kho_stats['Tổng COD'].apply(lambda x: f"{x:,.0f} đ")
        print(kho_stats.sort_values(by='Số đơn', ascending=False).head(15).to_string(index=False))
        
    print("\n-- Phân loại Trạng thái hiện tại:")
    if 'Trạng thái hiện tại' in df.columns:
        print(df['Trạng thái hiện tại'].value_counts().to_string())
        
    if 'Trạng Thái' in df.columns:
        tt_vc = df['Trạng Thái'].value_counts()
        print("\n-- Cột Trạng Thái (Tiến độ xử lý/Tick):")
        print(tt_vc.to_string())
            
    if 'Người tick GTC' in df.columns:
        tick_vc = df['Người tick GTC'].value_counts()
        print("\n-- Người tick GTC:")
        print(tick_vc.to_string())
            
    print("\n-- Phân loại Nhóm Rule:")
    if 'Nhóm rule' in df.columns:
        print(df['Nhóm rule'].value_counts().to_string())
        
    print("\n-- Lý do thất bại lần cuối:")
    if 'Lý do thất bại lần cuối' in df.columns:
        print(df['Lý do thất bại lần cuối'].value_counts().head(7).to_string())
        
    return df

print(">>> PHÂN TÍCH SHEET 22-10 (THEO LINK CỦA USER):")
df_22 = analyze_sheet('22-10')

print("\n\n>>> PHÂN TÍCH SHEET GẦN NHẤT 26-10:")
df_26 = analyze_sheet('26-10')

print("\n\n>>> PHÂN TÍCH SHEET import:")
df_import = analyze_sheet('import')
