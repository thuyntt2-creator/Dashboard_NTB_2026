import sys, os, pandas as pd, numpy as np
sys.path.insert(0, '.')
sys.stdout.reconfigure(encoding='utf-8')

import app
app.update_all_caches()

def safe_to_numeric(series):
    return pd.to_numeric(series.astype(str).str.replace(',', '.').str.strip(), errors='coerce').fillna(0.0)

def test_heavy_processor():
    df_ops = app.safe_read_csv(app.resolve_path('ops_heavy_10kg.csv', write=False))
    df_tao = app.safe_read_csv(app.resolve_path('ops_tao_don_10kg.csv', write=False))

    print(f"Loaded ops_heavy_10kg rows: {len(df_ops) if df_ops is not None else 0}")
    print(f"Loaded ops_tao_don_10kg rows: {len(df_tao) if df_tao is not None else 0}")

    if df_ops is None or df_tao is None:
        return {"error": "Missing ops_heavy_10kg.csv or ops_tao_don_10kg.csv"}

    # Process Ops
    df_ops.columns = [c.strip() for c in df_ops.columns]
    df_ops['Volume'] = safe_to_numeric(df_ops['Volume'])
    df_ops['% GTC'] = app.normalize_pct_col(df_ops['% GTC']) if '% GTC' in df_ops.columns else 0.0
    df_ops['% Gán'] = app.normalize_pct_col(df_ops['% Gán']) if '% Gán' in df_ops.columns else 0.0
    df_ops['Leadtime'] = safe_to_numeric(df_ops['Leadtime']) if 'Leadtime' in df_ops.columns else 0.0
    
    if 'Sản Lượng Giao Thành Công' in df_ops.columns:
        df_ops['delivered_vol'] = safe_to_numeric(df_ops['Sản Lượng Giao Thành Công'])
    else:
        df_ops['delivered_vol'] = df_ops['Volume'] * df_ops['% GTC']

    chi_tiet_col = next((c for c in df_ops.columns if c.lower() in ['chi tiết', 'bưu cục', 'buucuc', 'bc']), 'Chi tiết')
    df_ops['clean_bc'] = df_ops[chi_tiet_col].apply(app.clean_str)
    prov_col = next((df_ops[c] for c in df_ops.columns if c.lower() in ['tỉnh', 'tinh']), pd.Series("Không xác định", index=df_ops.index))
    am_col = next((df_ops[c] for c in df_ops.columns if c.lower() in ['am', 'am_name']), pd.Series("Không xác định", index=df_ops.index))
    
    df_ops['mapped_prov'] = df_ops['clean_bc'].map(app.BC_TO_PROV if hasattr(app, 'BC_TO_PROV') else {}).replace({'': np.nan}).fillna(prov_col).fillna("Không xác định")
    df_ops['mapped_am'] = df_ops['clean_bc'].map(app.BC_TO_AM if hasattr(app, 'BC_TO_AM') else {}).replace({'': np.nan}).fillna(am_col).fillna("Không xác định")

    total_ops_vol = float(df_ops['Volume'].sum())
    total_delivered = float(df_ops['delivered_vol'].sum())
    overall_gtc = round((total_delivered / total_ops_vol * 100), 2) if total_ops_vol > 0 else 0.0
    avg_leadtime = round(float(df_ops[df_ops['Leadtime'] > 0]['Leadtime'].mean()), 2) if len(df_ops[df_ops['Leadtime'] > 0]) > 0 else 0.0

    # Process Creation
    df_tao.columns = [c.strip() for c in df_tao.columns]
    vol_col = next((c for c in df_tao.columns if c.lower() in ['vol', 'volume', 'sản lượng']), 'vol')
    kl_col = next((c for c in df_tao.columns if c.lower() in ['kl_kg', 'khối lượng', 'khoi_luong']), 'kl_kg')
    wh_col = next((c for c in df_tao.columns if c.lower() in ['warehouse_name', 'bưu cục', 'buucuc', 'bc']), 'warehouse_name')
    kg_col = next((c for c in df_tao.columns if c.lower() in ['nhom_kg', 'nhóm kg']), 'nhom_kg')
    kh_col = next((c for c in df_tao.columns if c.lower() in ['nhom_kh', 'nhóm kh']), 'nhom_kh')

    df_tao['vol'] = safe_to_numeric(df_tao[vol_col])
    df_tao['kl_kg'] = safe_to_numeric(df_tao[kl_col])
    df_tao['clean_bc'] = df_tao[wh_col].apply(app.clean_str)
    
    total_created_vol = float(df_tao['vol'].sum())
    total_created_weight_kg = float(df_tao['kl_kg'].sum())
    total_created_weight_ton = round(total_created_weight_kg / 1000.0, 2)

    # Weight bracket summary
    kg_grp = df_tao.groupby(kg_col).agg({'vol': 'sum', 'kl_kg': 'sum'}).reset_index()
    kg_grp['pct_vol'] = (kg_grp['vol'] / total_created_vol * 100).round(2) if total_created_vol > 0 else 0.0
    kg_summary = kg_grp.to_dict(orient='records')

    print(f"Summary -> Total Ops Vol: {total_ops_vol}, GTC: {overall_gtc}%, Leadtime: {avg_leadtime}h")
    print(f"Creation -> Total Vol: {total_created_vol}, Weight: {total_created_weight_ton} Tấn")
    print("Weight Bracket Summary:", kg_summary)

test_heavy_processor()
