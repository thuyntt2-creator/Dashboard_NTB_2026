import sys
import json
import os
import pandas as pd
import numpy as np
from google.oauth2.credentials import Credentials
import gspread

sys.stdout.reconfigure(encoding='utf-8')

def build_ktc_data():
    print("=== 1. BUILDING KTC BACKLOG DATA ===")
    # Data from Image 1
    # Table 1: Đơn treo LUÂN CHUYỂN giao/trả trên 36h (Chưa/Không cần đóng kiện) theo AM
    backlog_by_am = [
        {
            "am": "Nguyễn Tiến Lực",
            "h0_6": 6290, "h6_12": 128, "h12_24": 77, "h24_36": 10,
            "h36_72": 2, "h72_120": 3, "h120_192": 0, "h192_plus": 0,
            "treo_36h": 381, "total": 6510, "diff": 6129
        },
        {
            "am": "Nguyễn Minh Hoàng",
            "h0_6": 2851, "h6_12": 1889, "h12_24": 73, "h24_36": 12,
            "h36_72": 4, "h72_120": 0, "h120_192": 0, "h192_plus": 0,
            "treo_36h": 0, "total": 4829, "diff": 4829
        },
        {
            "am": "Nguyễn Ngọc Khánh",
            "h0_6": 2545, "h6_12": 912, "h12_24": 167, "h24_36": 5,
            "h36_72": 4, "h72_120": 1, "h120_192": 0, "h192_plus": 0,
            "treo_36h": 0, "total": 3634, "diff": 3634
        },
        {
            "am": "Trương Quang Linh",
            "h0_6": 623, "h6_12": 611, "h12_24": 0, "h24_36": 0,
            "h36_72": 0, "h72_120": 0, "h120_192": 0, "h192_plus": 0,
            "treo_36h": 0, "total": 1234, "diff": 1234
        }
    ]
    tot_am = {
        "am": "TỔNG TOÀN VÙNG",
        "h0_6": sum(x["h0_6"] for x in backlog_by_am),
        "h6_12": sum(x["h6_12"] for x in backlog_by_am),
        "h12_24": sum(x["h12_24"] for x in backlog_by_am),
        "h24_36": sum(x["h24_36"] for x in backlog_by_am),
        "h36_72": sum(x["h36_72"] for x in backlog_by_am),
        "h72_120": sum(x["h72_120"] for x in backlog_by_am),
        "h120_192": sum(x["h120_192"] for x in backlog_by_am),
        "h192_plus": sum(x["h192_plus"] for x in backlog_by_am),
        "treo_36h": sum(x["treo_36h"] for x in backlog_by_am),
        "total": sum(x["total"] for x in backlog_by_am),
        "diff": sum(x["diff"] for x in backlog_by_am)
    }

    # Table 2: Backlog KTC theo Kho/Bưu cục
    backlog_by_kho = [
        {
            "kho": "Kho Trung Chuyển Khánh Hòa",
            "am": "Nguyễn Tiến Lực",
            "h0_6": 6290, "h6_12": 128, "h12_24": 77, "h24_36": 10,
            "h36_72": 2, "h72_120": 3, "h120_192": 0, "h192_plus": 0,
            "treo_36h": 381, "total": 6510, "diff": 6129
        },
        {
            "kho": "Kho Chuyển Tiếp Bình Thuận",
            "am": "Nguyễn Ngọc Khánh",
            "h0_6": 2545, "h6_12": 912, "h12_24": 167, "h24_36": 5,
            "h36_72": 4, "h72_120": 1, "h120_192": 0, "h192_plus": 0,
            "treo_36h": 0, "total": 3634, "diff": 3634
        },
        {
            "kho": "Kho Chuyển Tiếp Bảo Lộc - Lâm Đồng",
            "am": "Nguyễn Minh Hoàng",
            "h0_6": 899, "h6_12": 1831, "h12_24": 0, "h24_36": 0,
            "h36_72": 0, "h72_120": 0, "h120_192": 0, "h192_plus": 0,
            "treo_36h": 0, "total": 2730, "diff": 2730
        },
        {
            "kho": "Kho Chuyển Tiếp Đức Trọng - Lâm Đồng",
            "am": "Nguyễn Minh Hoàng",
            "h0_6": 1952, "h6_12": 58, "h12_24": 73, "h24_36": 12,
            "h36_72": 4, "h72_120": 0, "h120_192": 0, "h192_plus": 0,
            "treo_36h": 0, "total": 2099, "diff": 2099
        },
        {
            "kho": "Kho Chuyển Tiếp Đắk Nông",
            "am": "Trương Quang Linh",
            "h0_6": 623, "h6_12": 611, "h12_24": 0, "h24_36": 0,
            "h36_72": 0, "h72_120": 0, "h120_192": 0, "h192_plus": 0,
            "treo_36h": 0, "total": 1234, "diff": 1234
        }
    ]
    tot_kho = {
        "kho": "TỔNG CỘNG (5 KTC/KCT)",
        "am": "Toàn Vùng",
        "h0_6": sum(x["h0_6"] for x in backlog_by_kho),
        "h6_12": sum(x["h6_12"] for x in backlog_by_kho),
        "h12_24": sum(x["h12_24"] for x in backlog_by_kho),
        "h24_36": sum(x["h24_36"] for x in backlog_by_kho),
        "h36_72": sum(x["h36_72"] for x in backlog_by_kho),
        "h72_120": sum(x["h72_120"] for x in backlog_by_kho),
        "h120_192": sum(x["h120_192"] for x in backlog_by_kho),
        "h192_plus": sum(x["h192_plus"] for x in backlog_by_kho),
        "treo_36h": sum(x["treo_36h"] for x in backlog_by_kho),
        "total": sum(x["total"] for x in backlog_by_kho),
        "diff": sum(x["diff"] for x in backlog_by_kho)
    }

    # Table 3: Đơn treo LUÂN CHUYỂN giao/trả >24h – Mốc 7h30 hằng ngày
    trend_dates = ["31/08", "01/09", "02/09", "03/09", "04/09", "05/09", "06/09", "07/09"]
    trend_by_am = [
        {
            "am": "Nguyễn Tiến Lực",
            "d_31_08": 106,
            "d_01_09": {"val": 180, "diff": 74, "pct": 0.70},
            "d_02_09": {"val": 51, "diff": -129, "pct": -0.72},
            "d_03_09": {"val": 24, "diff": -27, "pct": -0.53},
            "d_04_09": {"val": 16, "diff": -8, "pct": -0.33},
            "d_05_09": {"val": 12, "diff": -4, "pct": -0.25},
            "d_06_09": {"val": 0, "diff": -12, "pct": -1.00},
            "d_07_09": {"val": 23, "diff": 23, "pct": 1.00}
        },
        {
            "am": "Nguyễn Minh Hoàng",
            "d_31_08": 12,
            "d_01_09": {"val": 11, "diff": -1, "pct": -0.08},
            "d_02_09": {"val": 23, "diff": 12, "pct": 1.09},
            "d_03_09": {"val": 5, "diff": -18, "pct": -0.78},
            "d_04_09": {"val": 5, "diff": 0, "pct": 0.00},
            "d_05_09": {"val": 13, "diff": 8, "pct": 1.60},
            "d_06_09": {"val": 0, "diff": -13, "pct": -1.00},
            "d_07_09": {"val": 38, "diff": 38, "pct": 1.00}
        },
        {
            "am": "Nguyễn Ngọc Khánh",
            "d_31_08": 22,
            "d_01_09": {"val": 7, "diff": -15, "pct": -0.68},
            "d_02_09": {"val": 5, "diff": -2, "pct": -0.29},
            "d_03_09": {"val": 5, "diff": 0, "pct": 0.00},
            "d_04_09": {"val": 5, "diff": 0, "pct": 0.00},
            "d_05_09": {"val": 13, "diff": 8, "pct": 1.60},
            "d_06_09": {"val": 0, "diff": -13, "pct": -1.00},
            "d_07_09": {"val": 18, "diff": 18, "pct": 1.00}
        },
        {
            "am": "Trương Quang Linh",
            "d_31_08": 0,
            "d_01_09": {"val": 0, "diff": 0, "pct": 0.00},
            "d_02_09": {"val": 0, "diff": 0, "pct": 0.00},
            "d_03_09": {"val": 2, "diff": 2, "pct": 1.00},
            "d_04_09": {"val": 0, "diff": -2, "pct": -1.00},
            "d_05_09": {"val": 0, "diff": 0, "pct": 0.00},
            "d_06_09": {"val": 0, "diff": 0, "pct": 0.00},
            "d_07_09": {"val": 1, "diff": 1, "pct": 1.00}
        }
    ]
    tot_trend = {
        "am": "TỔNG VÙNG",
        "d_31_08": 140,
        "d_01_09": {"val": 198, "diff": 58, "pct": 0.41},
        "d_02_09": {"val": 79, "diff": -119, "pct": -0.60},
        "d_03_09": {"val": 36, "diff": -43, "pct": -0.54},
        "d_04_09": {"val": 26, "diff": -10, "pct": -0.28},
        "d_05_09": {"val": 38, "diff": 12, "pct": 0.46},
        "d_06_09": {"val": 0, "diff": -38, "pct": -1.00},
        "d_07_09": {"val": 80, "diff": 80, "pct": 1.00}
    }

    print("=== 2. BUILDING LEADTIME DATA FROM SHEET_RAW.CSV ===")
    df_raw = pd.read_csv('sheet_raw.csv')
    
    # Let's extract Leadtime summary by Kho for W36 and for latest day
    def calc_leadtime(sub_df):
        rows = []
        for (loai_kho, ten_kho), grp in sub_df.groupby(['loai_kho', 'ten_kho']):
            tot_orders = int(grp['orders'].sum())
            t12 = int(grp['vol_12'].sum())
            t24 = int(grp['vol_24'].sum())
            pct12 = (t12 / tot_orders * 100) if tot_orders > 0 else 0
            pct24 = (t24 / tot_orders * 100) if tot_orders > 0 else 0
            # Weighted LT average
            lt_tb = (grp['lt_nhan_xuat'] * grp['orders']).sum() / tot_orders if tot_orders > 0 else 0
            lt_p50 = float(grp['lt_p50'].median())
            lt_p95 = float(grp['lt_95'].median())
            rows.append({
                "loai_kho": loai_kho,
                "ten_kho": ten_kho,
                "total_orders": tot_orders,
                "ton_12h": t12,
                "pct_12h": round(pct12, 2),
                "ton_24h": t24,
                "pct_24h": round(pct24, 2),
                "lt_tb": round(lt_tb, 2),
                "lt_p50": round(lt_p50, 2),
                "lt_p95": round(lt_p95, 2)
            })
        # Sort KTC first, then by total_orders desc
        rows.sort(key=lambda x: (x['loai_kho'], -x['total_orders']))
        # Grand total
        tot_all = sum(r['total_orders'] for r in rows)
        t12_all = sum(r['ton_12h'] for r in rows)
        t24_all = sum(r['ton_24h'] for r in rows)
        lt_tb_all = sum(r['lt_tb'] * r['total_orders'] for r in rows) / tot_all if tot_all > 0 else 0
        grand_total = {
            "loai_kho": "---",
            "ten_kho": "GRAND TOTAL",
            "total_orders": tot_all,
            "ton_12h": t12_all,
            "pct_12h": round(t12_all / tot_all * 100, 2) if tot_all > 0 else 0,
            "ton_24h": t24_all,
            "pct_24h": round(t24_all / tot_all * 100, 2) if tot_all > 0 else 0,
            "lt_tb": round(lt_tb_all, 2),
            "lt_p50": round(float(np.median([r['lt_p50'] for r in rows])), 2),
            "lt_p95": round(float(np.median([r['lt_p95'] for r in rows])), 2)
        }
        return {"items": rows, "total": grand_total}

    # W36 Leadtime
    w36_raw = df_raw[df_raw['week_num'] == 36]
    leadtime_w36 = calc_leadtime(w36_raw)

    # Leadtime from Image 2 (Single Day Snapshot - 31,542 orders)
    # Khánh Hòa: 12,880 | Bình Thuận: 11,028 | Đức Trọng: 4,362 | Đắk Nông: 3,272
    leadtime_snapshot = {
        "items": [
            {
                "loai_kho": "01. KTC",
                "ten_kho": "Kho Trung Chuyển Khánh Hòa",
                "total_orders": 12880,
                "ton_12h": 163, "pct_12h": 1.3,
                "ton_24h": 19, "pct_24h": 0.1,
                "lt_tb": 3.12, "lt_p50": 1.80, "lt_p95": 8.20
            },
            {
                "loai_kho": "02. KCT",
                "ten_kho": "Kho Chuyển Tiếp Bình Thuận",
                "total_orders": 11028,
                "ton_12h": 79, "pct_12h": 0.7,
                "ton_24h": 20, "pct_24h": 0.2,
                "lt_tb": 3.19, "lt_p50": 2.67, "lt_p95": 5.98
            },
            {
                "loai_kho": "02. KCT",
                "ten_kho": "Kho Chuyển Tiếp Đức Trọng - Lâm Đồng",
                "total_orders": 4362,
                "ton_12h": 15, "pct_12h": 0.3,
                "ton_24h": 1, "pct_24h": 0.0,
                "lt_tb": 2.88, "lt_p50": 3.75, "lt_p95": 5.43
            },
            {
                "loai_kho": "02. KCT",
                "ten_kho": "Kho Chuyển Tiếp Đắk Nông",
                "total_orders": 3272,
                "ton_12h": 405, "pct_12h": 12.4,
                "ton_24h": 6, "pct_24h": 0.2,
                "lt_tb": 4.99, "lt_p50": 0.91, "lt_p95": 17.06
            }
        ],
        "total": {
            "loai_kho": "---",
            "ten_kho": "GRAND TOTAL",
            "total_orders": 31542,
            "ton_12h": 662, "pct_12h": 2.1,
            "ton_24h": 46, "pct_24h": 0.1,
            "lt_tb": 3.31, "lt_p50": 2.24, "lt_p95": 7.09
        }
    }

    print("=== 3. BUILDING FILL RATE (TỶ LỆ LẤP ĐẦY XE) DATA ===")
    creds = Credentials.from_authorized_user_file('authorized_user.json')
    gc = gspread.authorize(creds)
    sh = gc.open_by_key('1rfoi8QaZSZNiYf8IyKNN4QLrjAVxCCGrX9Yli0D8T84')
    ws = sh.worksheet('DATA XỬ LÝ')
    df_fill = pd.DataFrame(ws.get_all_records())
    df_fill['Ngày_dt'] = pd.to_datetime(df_fill['Ngày'], errors='coerce')
    df_fill['tld_val'] = df_fill['TLLĐ chuyến (kg)'].str.rstrip('%').astype(float)

    # 3.1 Daily Comparison 05/09 vs 06/09 (Image 3)
    d05 = df_fill[df_fill['Ngày_dt'] == '2026-09-05']
    d06 = df_fill[df_fill['Ngày_dt'] == '2026-09-06']

    kho_list = [
        "Kho Trung Chuyển Khánh Hòa",
        "Kho Chuyển Tiếp Đức Trọng - Lâm Đồng",
        "Kho Chuyển Tiếp Đắk Nông",
        "Kho Chuyển Tiếp Bình Thuận",
        "Kho Chuyển Tiếp Bảo Lộc - Lâm Đồng"
    ]
    kho_short_map = {
        "Kho Trung Chuyển Khánh Hòa": "KTC Khánh Hòa",
        "Kho Chuyển Tiếp Đức Trọng - Lâm Đồng": "KCT Đức Trọng-Lâm Đồng",
        "Kho Chuyển Tiếp Đắk Nông": "KCT Đắk Nông",
        "Kho Chuyển Tiếp Bình Thuận": "KCT Bình Thuận",
        "Kho Chuyển Tiếp Bảo Lộc - Lâm Đồng": "KCT Bảo Lộc-Lâm Đồng"
    }

    daily_rows = []
    for full_name, short_name in kho_short_map.items():
        s05 = d05[d05['Kho'] == short_name]
        s06 = d06[d06['Kho'] == short_name]
        chuyen_05 = len(s05)
        chuyen_06 = len(s06)
        diff_chuyen = chuyen_06 - chuyen_05
        tld_05 = round(s05['tld_val'].mean(), 1)
        tld_06 = round(s06['tld_val'].mean(), 1)
        diff_tld = round(tld_06 - tld_05, 1)
        c10 = len(s06[s06['tld_val'] < 10])
        c20 = len(s06[(s06['tld_val'] >= 10) & (s06['tld_val'] < 20)])
        c30 = len(s06[(s06['tld_val'] >= 20) & (s06['tld_val'] < 30)])
        daily_rows.append({
            "kho": full_name,
            "short_name": short_name,
            "chuyen_05": chuyen_05,
            "chuyen_06": chuyen_06,
            "diff_chuyen": diff_chuyen,
            "tld_05": tld_05,
            "tld_06": tld_06,
            "diff_tld": diff_tld,
            "u10": c10,
            "u20": c20,
            "u30": c30
        })

    tot_d05 = len(d05)
    tot_d06 = len(d06)
    tot_tld05 = round(d05['tld_val'].mean(), 1)
    tot_tld06 = round(d06['tld_val'].mean(), 1)
    daily_total = {
        "kho": "TỔNG CỘNG (5 KTC)",
        "short_name": "Toàn Vùng",
        "chuyen_05": tot_d05,
        "chuyen_06": tot_d06,
        "diff_chuyen": tot_d06 - tot_d05,
        "tld_05": tot_tld05,
        "tld_06": tot_tld06,
        "diff_tld": round(tot_tld06 - tot_tld05, 1),
        "u10": sum(r['u10'] for r in daily_rows),
        "u20": sum(r['u20'] for r in daily_rows),
        "u30": sum(r['u30'] for r in daily_rows)
    }

    # 3.2 Weekly Comparison W35 vs W36 (Newly Calculated!)
    w35 = df_fill[(df_fill['Ngày_dt'] >= '2026-08-24') & (df_fill['Ngày_dt'] <= '2026-08-30')]
    w36 = df_fill[(df_fill['Ngày_dt'] >= '2026-08-31') & (df_fill['Ngày_dt'] <= '2026-09-06')]

    weekly_rows = []
    for full_name, short_name in kho_short_map.items():
        s35 = w35[w35['Kho'] == short_name]
        s36 = w36[w36['Kho'] == short_name]
        c35 = len(s35)
        c36 = len(s36)
        diff_c = c36 - c35
        tld_35 = round(s35['tld_val'].mean(), 1)
        tld_36 = round(s36['tld_val'].mean(), 1)
        diff_tld_w = round(tld_36 - tld_35, 1)
        c10_w = len(s36[s36['tld_val'] < 10])
        c20_w = len(s36[(s36['tld_val'] >= 10) & (s36['tld_val'] < 20)])
        c30_w = len(s36[(s36['tld_val'] >= 20) & (s36['tld_val'] < 30)])
        c_under30 = c10_w + c20_w + c30_w
        weekly_rows.append({
            "kho": full_name,
            "short_name": short_name,
            "chuyen_w35": c35,
            "chuyen_w36": c36,
            "diff_chuyen": diff_c,
            "tld_w35": tld_35,
            "tld_w36": tld_36,
            "diff_tld": diff_tld_w,
            "under_30": c_under30,
            "u10": c10_w,
            "u20": c20_w,
            "u30": c30_w
        })

    tot_w35_c = len(w35)
    tot_w36_c = len(w36)
    tot_w35_tld = round(w35['tld_val'].mean(), 1)
    tot_w36_tld = round(w36['tld_val'].mean(), 1)
    weekly_total = {
        "kho": "TỔNG CỘNG (5 KTC)",
        "short_name": "Toàn Vùng",
        "chuyen_w35": tot_w35_c,
        "chuyen_w36": tot_w36_c,
        "diff_chuyen": tot_w36_c - tot_w35_c,
        "tld_w35": tot_w35_tld,
        "tld_w36": tot_w36_tld,
        "diff_tld": round(tot_w36_tld - tot_w35_tld, 1),
        "under_30": sum(r['under_30'] for r in weekly_rows),
        "u10": sum(r['u10'] for r in weekly_rows),
        "u20": sum(r['u20'] for r in weekly_rows),
        "u30": sum(r['u30'] for r in weekly_rows)
    }

    # 3.3 Historical 6-Week Trend (from Bao cao Tuan)
    weeks_trend = [
        {"week": "Tuần 30", "chuyen": 522, "tld": 43.5, "u10": 15, "u20": 58, "u30": 75, "under30": 148, "diff": 0.0},
        {"week": "Tuần 31", "chuyen": 521, "tld": 46.6, "u10": 16, "u20": 50, "u30": 71, "under30": 137, "diff": 3.1},
        {"week": "Tuần 32", "chuyen": 545, "tld": 48.7, "u10": 17, "u20": 37, "u30": 70, "under30": 124, "diff": 2.1},
        {"week": "Tuần 33", "chuyen": 562, "tld": 54.2, "u10": 15, "u20": 38, "u30": 39, "under30": 92, "diff": 5.5},
        {"week": "Tuần 34", "chuyen": 547, "tld": 48.0, "u10": 26, "u20": 34, "u30": 61, "under30": 121, "diff": -6.2},
        {"week": "Tuần 35", "chuyen": 538, "tld": 51.8, "u10": 14, "u20": 26, "u30": 53, "under30": 93, "diff": 3.8},
        {"week": "Tuần 36", "chuyen": 516, "tld": 48.1, "u10": 10, "u20": 40, "u30": 62, "under30": 112, "diff": -3.7}
    ]

    # 3.4 Key Causes for <30% Fill Rate (from Sheet Tuan 35 & W36 patterns)
    causes_analysis = [
        {"cause": "Sản lượng bưu cục / hàng lấy về thấp", "kh": 3, "dt": 8, "dn": 19, "bt": 0, "bl": 3, "total": 33, "share": 35.1},
        {"cause": "Lộ trình ghé nhiều điểm / quãng đường dài nhưng ít hàng", "kh": 0, "dt": 4, "dn": 0, "bt": 7, "bl": 0, "total": 11, "share": 11.7},
        {"cause": "Chủ động giữ hàng / ghép điểm để tối ưu (giảm chuyến khác)", "kh": 0, "dt": 8, "dn": 0, "bt": 0, "bl": 0, "total": 8, "share": 8.5},
        {"cause": "Vấn đề vận hành khác (xe trễ, lộ trình bất hợp lý...)", "kh": 1, "dt": 1, "dn": 0, "bt": 5, "bl": 0, "total": 7, "share": 7.4},
        {"cause": "Sản lượng giảm theo chu kỳ tuần (đầu/cuối tuần)", "kh": 3, "dt": 1, "dn": 0, "bt": 0, "bl": 2, "total": 6, "share": 6.4},
        {"cause": "Xe trọng tải 5.000kg không đủ hàng để ghép đầy", "kh": 0, "dt": 0, "dn": 0, "bt": 0, "bl": 5, "total": 5, "share": 5.3},
        {"cause": "Chuyến gom hàng bưu cục (đặc thù, TLLĐ thấp theo thiết kế)", "kh": 5, "dt": 0, "dn": 0, "bt": 0, "bl": 0, "total": 5, "share": 5.3},
        {"cause": "Chuyến bị hủy / xe phát sinh ngoài kế hoạch", "kh": 2, "dt": 0, "dn": 0, "bt": 3, "bl": 2, "total": 7, "share": 7.4},
        {"cause": "Khác / chưa rõ nguyên nhân", "kh": 6, "dt": 2, "dn": 1, "bt": 1, "bl": 0, "total": 10, "share": 10.6}
    ]

    ktc_final = {
        "backlog": {
            "by_am": backlog_by_am,
            "total_am": tot_am,
            "by_kho": backlog_by_kho,
            "total_kho": tot_kho,
            "trend_dates": trend_dates,
            "trend_by_am": trend_by_am,
            "total_trend": tot_trend
        },
        "leadtime": {
            "snapshot": leadtime_snapshot,
            "w36": leadtime_w36
        },
        "fill_rate": {
            "daily": {
                "date_comp": "05/09/2026 vs 06/09/2026",
                "items": daily_rows,
                "total": daily_total
            },
            "weekly": {
                "week_comp": "Tuần W35 vs Tuần W36 (24/08 – 06/09/2026)",
                "items": weekly_rows,
                "total": weekly_total
            },
            "trend_6w": weeks_trend,
            "causes": causes_analysis
        }
    }

    os.makedirs('scratch', exist_ok=True)
    with open('scratch/ktc_processed.json', 'w', encoding='utf-8') as f:
        json.dump(ktc_final, f, ensure_ascii=False, indent=2)
    print("🎉 SUCCESS: Generated scratch/ktc_processed.json successfully!")
    return ktc_final

if __name__ == '__main__':
    build_ktc_data()
