import json
import re
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

print("=== 1. PREPARING EXACT W38 FILL RATE DATA ===")
fill_rate_w38 = {
    "weekly": {
        "total": {
            "tld_curr": 51.0,
            "tld_prev": 54.8,
            "diff_tld": -3.8,
            "under_30": 76,
            "trips_curr": 523,
            "trips_prev": 551,
            "diff_chuyen": -28,
            "u10": 7,
            "u20": 32,
            "u30": 37,
            "tld_w38": 51.0,
            "tld_w37": 54.8
        },
        "items": [
            {
                "kho": "Kho Trung Chuyển Khánh Hòa",
                "short_name": "KTC Khánh Hòa",
                "chuyen_prev": 212,
                "chuyen_curr": 202,
                "diff_chuyen": -10,
                "tld_prev": 60.9,
                "tld_curr": 57.1,
                "diff_tld": -3.8,
                "under_30": 13
            },
            {
                "kho": "Kho Chuyển Tiếp Bình Thuận",
                "short_name": "KCT Bình Thuận",
                "chuyen_prev": 130,
                "chuyen_curr": 114,
                "diff_chuyen": -16,
                "tld_prev": 55.1,
                "tld_curr": 51.3,
                "diff_tld": -3.7,
                "under_30": 14
            },
            {
                "kho": "Kho Chuyển Tiếp Đức Trọng - Lâm Đồng",
                "short_name": "KCT Đức Trọng-Lâm Đồng",
                "chuyen_prev": 106,
                "chuyen_curr": 109,
                "diff_chuyen": 3,
                "tld_prev": 53.7,
                "tld_curr": 47.9,
                "diff_tld": -5.8,
                "under_30": 23
            },
            {
                "kho": "Kho Chuyển Tiếp Bảo Lộc - Lâm Đồng",
                "short_name": "KCT Bảo Lộc-Lâm Đồng",
                "chuyen_prev": 59,
                "chuyen_curr": 54,
                "diff_chuyen": -5,
                "tld_prev": 46.3,
                "tld_curr": 45.7,
                "diff_tld": -0.7,
                "under_30": 6
            },
            {
                "kho": "Kho Chuyển Tiếp Đắk Nông",
                "short_name": "KCT Đắk Nông",
                "chuyen_prev": 44,
                "chuyen_curr": 44,
                "diff_chuyen": 0,
                "tld_prev": 38.7,
                "tld_curr": 37.0,
                "diff_tld": -1.7,
                "under_30": 20
            }
        ]
    },
    "history": [
        { "week": "T33 (10/08-16/08)", "trips": 562, "rate": 0.542, "low_trips": 92 },
        { "week": "T34 (17/08-23/08)", "trips": 547, "rate": 0.480, "low_trips": 121 },
        { "week": "T35 (24/08-30/08)", "trips": 538, "rate": 0.518, "low_trips": 93 },
        { "week": "T36 (31/08-06/09)", "trips": 516, "rate": 0.481, "low_trips": 112 },
        { "week": "T37 (07/09-13/09)", "trips": 551, "rate": 0.548, "low_trips": 79 },
        { "week": "T38 (14/09-20/09)", "trips": 523, "rate": 0.510, "low_trips": 76 }
    ],
    "trend_6w": [
        { "week": "T33", "rate": 54.2, "trips": 562, "under30": 92 },
        { "week": "T34", "rate": 48.0, "trips": 547, "under30": 121 },
        { "week": "T35", "rate": 51.8, "trips": 538, "under30": 93 },
        { "week": "T36", "rate": 48.1, "trips": 516, "under30": 112 },
        { "week": "T37", "rate": 54.8, "trips": 551, "under30": 79 },
        { "week": "T38", "rate": 51.0, "trips": 523, "under30": 76 }
    ]
}

# --- 2. UPDATE data.js & data.json ---
print("=== 2. UPDATING data.js AND data.json ===")
with open('data.js', 'r', encoding='utf-8') as f:
    text = f.read()

prefix = "window.DASHBOARD_DATA = "
data = json.loads(text[len(prefix):].rstrip(';\n '))

if 'ktc' not in data:
    data['ktc'] = {}

data['ktc']['fill_rate'] = fill_rate_w38

# Save back to data.js
new_content = prefix + json.dumps(data, ensure_ascii=False, indent=2) + ";\n"
with open('data.js', 'w', encoding='utf-8') as f:
    f.write(new_content)
print(f"Updated data.js ({len(new_content)} chars)")

# Save to data.json
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print("Updated data.json")

print("=== 3. SUCCESS ===")
