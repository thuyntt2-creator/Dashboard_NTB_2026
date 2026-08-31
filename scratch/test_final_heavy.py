import os, sys, re, json
import pandas as pd
import numpy as np

sys.stdout.reconfigure(encoding='utf-8')

def is_ck_po(name):
    if not name or pd.isna(name):
        return False
    s = str(name).strip().lower()
    return bool(re.search(r'(^|\s|\(|\/|-)ck(\s|\)|\/|-|$)|bcck|cồng kềnh|cong kenh', s))

def safe_to_numeric(series):
    if series is None: return pd.Series([], dtype=float)
    return pd.to_numeric(series.astype(str).str.replace('%', '', regex=False).str.replace(',', '', regex=False).str.strip(), errors='coerce').fillna(0.0)

def normalize_pct_col(series):
    nums = safe_to_numeric(series)
    return np.where(nums > 1.0, nums, nums * 100.0)

def clean_str(val):
    if pd.isna(val) or val is None:
        return ""
    import unicodedata
    s = str(val).strip().lower()
    s = unicodedata.normalize('NFC', s)
    s = re.sub(r'[\(\)\[\]\-_,.]', ' ', s)
    return ' '.join(s.split())

def test_process_heavy_report(am=None, province=None, post_office=None, date=None, ck_only=False):
    # Read files
    df_ops = pd.read_csv("scratch/sheet_sl_10kg_raw.csv")
    df_tao = pd.read_csv("scratch/sheet_tren10kg_raw.csv")

    # Dates
    df_ops['date'] = df_ops['Time'].astype(str).apply(lambda x: x.split(' - ')[0].strip() if ' - ' in str(x) else str(x).strip())
    df_tao['date'] = df_tao['ngay_tao_don'].astype(str).str.strip()

    # Numbers
    df_ops['Volume'] = safe_to_numeric(df_ops['Volume'])
    df_ops['delivered_vol'] = safe_to_numeric(df_ops['Sản Lượng Giao Thành Công'])
    df_ops['Hàng Mới Về Trong Ngày'] = safe_to_numeric(df_ops['Hàng Mới Về Trong Ngày'])
    df_ops['Sản Lượng Tồn'] = safe_to_numeric(df_ops['Sản Lượng Tồn'])
    df_ops['Leadtime'] = safe_to_numeric(df_ops['Leadtime'])
    df_ops['% GTC'] = normalize_pct_col(df_ops['% GTC']) if '% GTC' in df_ops else np.where(df_ops['Volume']>0, (df_ops['delivered_vol']/df_ops['Volume']*100).round(2), 0.0)

    df_tao['so_don'] = safe_to_numeric(df_tao['so_don'])

    # PO names & CK flag
    df_ops['po_name'] = df_ops['Chi tiết'].fillna('Không xác định').astype(str).str.strip()
    df_tao['po_name'] = df_tao['warehouse_name'].fillna('Không xác định').astype(str).str.strip()

    df_ops['is_ck'] = df_ops['po_name'].apply(is_ck_po)
    df_tao['is_ck'] = df_tao['po_name'].apply(is_ck_po)

    # Standardize Tỉnh & AM
    df_ops['mapped_prov'] = df_ops['Tỉnh'].fillna('Không xác định')
    df_ops['mapped_am'] = df_ops['AM'].fillna('Không xác định')
    df_tao['mapped_prov'] = df_tao['province_name'].fillna('Không xác định')
    
    # Map AM to df_tao from df_ops mapping
    po_to_am = dict(zip(df_ops['po_name'], df_ops['mapped_am']))
    df_tao['mapped_am'] = df_tao['po_name'].map(po_to_am).fillna('Không xác định')

    # Available dates
    available_dates = sorted([d for d in df_ops['date'].unique() if re.match(r'^\d{4}-\d{2}-\d{2}$', d)])
    selected_date = date if (date and date in available_dates) else (available_dates[-1] if available_dates else None)

    # Baseline dates (up to 7 days before selected_date)
    prev_dates = [d for d in available_dates if d < selected_date][-7:]

    # Filter by CK if requested
    if ck_only:
        df_ops = df_ops[df_ops['is_ck'] == True]
        df_tao = df_tao[df_tao['is_ck'] == True]

    # Filter by AM / Province / PO
    if am and am != 'all':
        df_ops = df_ops[df_ops['mapped_am'] == am]
        df_tao = df_tao[df_tao['mapped_am'] == am]
    if province and province != 'all':
        df_ops = df_ops[df_ops['mapped_prov'] == province]
        df_tao = df_tao[df_tao['mapped_prov'] == province]
    if post_office and post_office != 'all':
        df_ops = df_ops[df_ops['po_name'] == post_office]
        df_tao = df_tao[df_tao['po_name'] == post_office]

    # 1. Overall Aggregates for selected_date
    ops_sel = df_ops[df_ops['date'] == selected_date] if selected_date else df_ops
    tao_sel = df_tao[df_tao['date'] == selected_date] if selected_date else df_tao

    total_ops_vol = float(ops_sel['Volume'].sum())
    total_delivered = float(ops_sel['delivered_vol'].sum())
    total_incoming = float(ops_sel['Hàng Mới Về Trong Ngày'].sum())
    total_ton = float(ops_sel['Sản Lượng Tồn'].sum())
    overall_gtc = round((total_delivered / total_ops_vol * 100), 2) if total_ops_vol > 0 else 0.0

    valid_lt = ops_sel[ops_sel['Leadtime'] > 0]['Leadtime']
    avg_leadtime = round(float(valid_lt.mean()), 2) if len(valid_lt) > 0 else 0.0

    total_created_vol = float(tao_sel['so_don'].sum())

    # 2. Baseline comparison for Selected Date
    ops_prev = df_ops[df_ops['date'].isin(prev_dates)]
    baseline_daily_vol = float(ops_prev['Volume'].sum() / max(len(prev_dates), 1)) if prev_dates else total_ops_vol
    vol_growth_pct = round(((total_ops_vol - baseline_daily_vol) / max(baseline_daily_vol, 1)) * 100, 1)

    # 3. BCCK Spotlight (Các bưu cục có tên CK)
    ck_ops_sel = ops_sel[ops_sel['is_ck'] == True]
    ck_tao_sel = tao_sel[tao_sel['is_ck'] == True]
    ck_total_ops_vol = float(ck_ops_sel['Volume'].sum())
    ck_total_delivered = float(ck_ops_sel['delivered_vol'].sum())
    ck_total_created = float(ck_tao_sel['so_don'].sum())
    ck_gtc = round((ck_total_delivered / ck_total_ops_vol * 100), 2) if ck_total_ops_vol > 0 else 0.0
    ck_share_pct = round((ck_total_ops_vol / total_ops_vol * 100), 1) if total_ops_vol > 0 else 0.0

    # 4. PO Summary & Surge Anomaly Analysis
    po_ops_sel = ops_sel.groupby(['po_name', 'mapped_prov', 'mapped_am', 'is_ck']).agg({
        'Volume': 'sum',
        'delivered_vol': 'sum',
        'Hàng Mới Về Trong Ngày': 'sum',
        'Sản Lượng Tồn': 'sum',
        'Leadtime': 'mean'
    }).reset_index().rename(columns={'Volume': 'vol_actual', 'delivered_vol': 'delivered_actual'})

    po_ops_prev = df_ops[df_ops['date'].isin(prev_dates)].groupby('po_name')['Volume'].mean().reset_index().rename(columns={'Volume': 'vol_avg_prev'})
    po_tao_sel = tao_sel.groupby('po_name')['so_don'].sum().reset_index().rename(columns={'so_don': 'vol_created'})
    po_tao_prev = df_tao[df_tao['date'].isin(prev_dates)].groupby('po_name')['so_don'].mean().reset_index().rename(columns={'so_don': 'vol_created_avg_prev'})

    po_merged = pd.merge(po_ops_sel, po_ops_prev, on='po_name', how='left')
    po_merged = pd.merge(po_merged, po_tao_sel, on='po_name', how='left')
    po_merged = pd.merge(po_merged, po_tao_prev, on='po_name', how='left')
    po_merged = po_merged.fillna({'vol_avg_prev': 0.0, 'vol_created': 0.0, 'vol_created_avg_prev': 0.0})

    po_merged['vol_diff'] = (po_merged['vol_actual'] - po_merged['vol_avg_prev']).round(1)
    po_merged['growth_pct'] = np.where(
        po_merged['vol_avg_prev'] > 0,
        ((po_merged['vol_actual'] - po_merged['vol_avg_prev']) / po_merged['vol_avg_prev'] * 100).round(1),
        np.where(po_merged['vol_actual'] > 0, 100.0, 0.0)
    )

    po_merged['gtc_pct'] = np.where(
        po_merged['vol_actual'] > 0,
        (po_merged['delivered_actual'] / po_merged['vol_actual'] * 100).round(1),
        0.0
    )
    po_merged['Leadtime'] = po_merged['Leadtime'].round(1)

    def classify_spike(r):
        g = r['growth_pct']
        d = r['vol_diff']
        if g >= 100 and d >= 15:
            return 'CRITICAL', '🔴 Đột biến cực đại (+{:.0f}%)'.format(g)
        elif (g >= 50 and d >= 10) or g >= 80:
            return 'HIGH', '🟠 Đột biến cao (+{:.0f}%)'.format(g)
        elif g >= 25 and d >= 5:
            return 'WARNING', '🟡 Tăng nhanh (+{:.0f}%)'.format(g)
        elif g <= -30:
            return 'DOWN', '📉 Giảm mạnh ({:.0f}%)'.format(g)
        else:
            return 'NORMAL', '🟢 Bình thường'

    po_merged['spike_level'], po_merged['spike_label'] = zip(*po_merged.apply(classify_spike, axis=1))

    # Sort default by vol_actual descending
    po_merged = po_merged.sort_values(by='vol_actual', ascending=False)

    # Surge counts
    critical_count = int((po_merged['spike_level'] == 'CRITICAL').sum())
    high_count = int((po_merged['spike_level'] == 'HIGH').sum())
    warning_count = int((po_merged['spike_level'] == 'WARNING').sum())
    total_surge_pos = critical_count + high_count

    # 5. Dual-Track Daily Trends (Created vs Actual Delivery)
    daily_ops = df_ops.groupby('date').agg({'Volume': 'sum', 'delivered_vol': 'sum'}).reset_index()
    daily_ops['gtc_pct'] = np.where(daily_ops['Volume'] > 0, (daily_ops['delivered_vol'] / daily_ops['Volume'] * 100).round(1), 0.0)

    daily_tao = df_tao.groupby('date')['so_don'].sum().reset_index().rename(columns={'so_don': 'vol_created'})

    daily_trend = pd.merge(daily_ops, daily_tao, on='date', how='outer').sort_values(by='date').fillna(0)

    # 6. Weight Brackets Breakdown from df_tao
    weight_summary = []
    if 'nhom_kl' in df_tao:
        w_grp = tao_sel.groupby('nhom_kl')['so_don'].sum().reset_index()
        w_grp['pct'] = np.where(total_created_vol > 0, (w_grp['so_don'] / total_created_vol * 100).round(1), 0.0)
        weight_summary = w_grp.to_dict(orient='records')

    # 7. Customer Groups Breakdown from df_tao
    customer_summary = []
    if 'nhom_kh' in df_tao:
        c_grp = tao_sel.groupby('nhom_kh')['so_don'].sum().reset_index()
        c_grp['pct'] = np.where(total_created_vol > 0, (c_grp['so_don'] / total_created_vol * 100).round(1), 0.0)
        customer_summary = c_grp.to_dict(orient='records')

    # 8. Top Spike POs (Top 5 highest growth)
    top_spikes = po_merged[po_merged['vol_actual'] >= 10].sort_values(by='growth_pct', ascending=False).head(5).to_dict(orient='records')

    # 9. Top & Worst % GTC POs
    po_gtc_valid = po_merged[po_merged['vol_actual'] >= 10]
    top_pos_gtc = po_gtc_valid.sort_values(by='gtc_pct', ascending=False).head(5).to_dict(orient='records')
    worst_pos_gtc = po_gtc_valid.sort_values(by='gtc_pct', ascending=True).head(5).to_dict(orient='records')

    # Unique PO list for filter
    po_list = sorted([str(p) for p in df_ops['po_name'].dropna().unique() if str(p) not in ['Grand Total', 'nan', 'none']])

    return {
        "selected_date": selected_date,
        "available_dates": available_dates,
        "total_ops_vol": total_ops_vol,
        "total_created_vol": total_created_vol,
        "total_incoming_vol": total_incoming,
        "total_ton_vol": total_ton,
        "overall_gtc": overall_gtc,
        "avg_leadtime": avg_leadtime,
        "vol_growth_pct": vol_growth_pct,
        "baseline_daily_vol": round(baseline_daily_vol, 1),
        "critical_count": critical_count,
        "high_count": high_count,
        "warning_count": warning_count,
        "total_surge_pos": total_surge_pos,
        "bcck_spotlight": {
            "ck_total_ops_vol": ck_total_ops_vol,
            "ck_total_created": ck_total_created,
            "ck_gtc": ck_gtc,
            "ck_share_pct": ck_share_pct,
            "ck_pos_count": len(po_merged[po_merged['is_ck'] == True]),
            "ck_pos": po_merged[po_merged['is_ck'] == True].to_dict(orient='records')
        },
        "po_ops_summary": po_merged.to_dict(orient='records'),
        "daily_trend": daily_trend.to_dict(orient='records'),
        "weight_bracket_summary": weight_summary,
        "customer_group_summary": customer_summary,
        "top_spikes": top_spikes,
        "top_pos": top_pos_gtc,
        "worst_pos": worst_pos_gtc,
        "po_list": po_list
    }

res = test_process_heavy_report()
print("Result keys:", res.keys())
print("Selected date:", res['selected_date'])
print("Total ops vol:", res['total_ops_vol'], "GTC:", res['overall_gtc'])
print("Total created vol:", res['total_created_vol'])
print("Total surge POs (Critical + High):", res['total_surge_pos'])
print("BCCK Spotlight:", res['bcck_spotlight'])
print("Top 3 Spikes:\n", pd.DataFrame(res['top_spikes'])[['po_name', 'vol_actual', 'vol_avg_prev', 'growth_pct', 'spike_label']])

