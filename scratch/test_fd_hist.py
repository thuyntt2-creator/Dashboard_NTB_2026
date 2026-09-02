import json
import datetime

def test_fd_history_logic():
    # Sample current FD data
    current_data = {
        "date": "01/09/2026",
        "summary": {
            "total_orders": 48871,
            "return_orders": 3405,
            "fd_rate": 6.97,
            "po_count": 84
        },
        "channels": [
            {"channel": "Shopee", "total_orders": 14505, "return_rate": 4.88}
        ],
        "am_rankings": [
            {"am": "AM Long", "total_orders": 1898, "return_orders": 266, "fd_rate": 14.0, "return_share": 7.81, "volume_share": 3.88}
        ],
        "all_pos": [
            {"post_office": "(LDO) Lang Biang - Đà Lạt 1", "am": "AM Đại", "total_orders": 390, "return_orders": 87, "fd_rate": 22.3, "return_share": 2.56}
        ]
    }
    
    # Snapshot format
    entry = {
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "date": current_data.get("date", ""),
        "summary": current_data.get("summary", {}),
        "am_map": {a["am"]: a for a in current_data.get("am_rankings", [])},
        "po_map": {p["post_office"]: p for p in current_data.get("all_pos", [])}
    }
    print("Snapshot created:", entry["timestamp"], entry["date"])
    print("AM map sample:", list(entry["am_map"].keys()))

test_fd_history_logic()
