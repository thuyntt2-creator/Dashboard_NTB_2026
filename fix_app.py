import sys, re
with open('app.py', 'r', encoding='utf-8') as f:
    code = f.read()

process_ca_code = '''
def process_ca_report():
    df = load_df_from_db('ops_ca_data.csv')
    if df is None or df.empty:
        return {"error": "Không tìm thấy dữ liệu báo cáo Ca."}
    
    col_map = {str(c).strip().lower(): c for c in df.columns}
    col_loai_hang = col_map.get('loại hàng', 'Loại Hàng')
    col_am = col_map.get('am', 'AM')
    col_bc = col_map.get('chi tiết', 'Chi tiết')
    if 'bưu cục' in col_map:
        col_bc = col_map['bưu cục']
        
    col_vol = col_map.get('volume', 'Volume')
    col_gtc = col_map.get('sản lượng giao thành công', 'Sản Lượng Giao Thành Công')
    
    if col_loai_hang not in df.columns or col_vol not in df.columns:
        return {"error": "Dữ liệu CA thiếu các cột cần thiết."}
        
    def clean_num(x):
        try:
            if pd.isna(x) or x == '': return 0
            return int(str(x).replace('.','').replace(',',''))
        except:
            return 0
            
    df[col_vol] = df[col_vol].apply(clean_num)
    df[col_gtc] = df[col_gtc].apply(clean_num)
    
    df = df[df[col_loai_hang].isin(['Hàng Mới Ca 1', 'Hàng Mới Ca 2', 'Hàng Tồn'])]
    
    if df.empty:
        return {"error": "Không có dữ liệu Hàng Mới Ca 1, Ca 2 hoặc Hàng Tồn."}
        
    pt_bc = df.pivot_table(index=[col_am, col_bc], columns=col_loai_hang, values=[col_vol, col_gtc], aggfunc='sum', fill_value=0)
    pt_bc.columns = [f"{c[1]}_{c[0]}" for c in pt_bc.columns]
    pt_bc = pt_bc.reset_index().rename(columns={col_am: "AM", col_bc: "Bưu Cục"})
    
    pt_am = df.pivot_table(index=[col_am], columns=col_loai_hang, values=[col_vol, col_gtc], aggfunc='sum', fill_value=0)
    pt_am.columns = [f"{c[1]}_{c[0]}" for c in pt_am.columns]
    pt_am = pt_am.reset_index().rename(columns={col_am: "AM"})
    
    return {
        "by_bc": clean_nan(pt_bc.to_dict(orient='records')),
        "by_am": clean_nan(pt_am.to_dict(orient='records'))
    }
'''

if 'def process_ca_report' not in code:
    code = code.replace(
        'def process_fd_report(am=None, province=None, post_office=None):',
        process_ca_code + '\ndef process_fd_report(am=None, province=None, post_office=None):'
    )

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(code)
print('Injected process_ca_report')
