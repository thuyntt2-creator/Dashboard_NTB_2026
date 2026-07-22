import sys
import json
import csv
import os

# Redirect standard print output to stderr to avoid corrupting the stdout JSON-RPC stream
def log(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)
    sys.stderr.flush()

def read_co_cau():
    """Reads co_cau_ntb.csv mapping warehouse_id -> Bưu cục, Tỉnh, AM"""
    data = {}
    if not os.path.exists('co_cau_ntb.csv'):
        log("Warning: co_cau_ntb.csv not found in current directory.")
        return data
    try:
        with open('co_cau_ntb.csv', 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                wh_id = row.get('warehouse_id', '').strip()
                if wh_id:
                    data[wh_id] = {
                        'name': row.get('Bưu cục', '').strip(),
                        'tinh': row.get('Tỉnh', '').strip(),
                        'am': row.get('AM', '').strip()
                    }
    except Exception as e:
        log(f"Error reading co_cau_ntb.csv: {e}")
    return data

def read_unstable_pos():
    """Reads buu_cuc_bat_on.csv starting from the column header row"""
    results = []
    if not os.path.exists('buu_cuc_bat_on.csv'):
        log("Warning: buu_cuc_bat_on.csv not found in current directory.")
        return results
    try:
        with open('buu_cuc_bat_on.csv', 'r', encoding='utf-8') as f:
            lines = f.readlines()
        # Find the line that starts the actual CSV table headers
        header_idx = -1
        for idx, line in enumerate(lines):
            if line.startswith('ngay,') or 'kho_giao_id' in line:
                header_idx = idx
                break
        if header_idx == -1:
            log("Error: Could not identify CSV headers in buu_cuc_bat_on.csv.")
            return results
        
        reader = csv.DictReader(lines[header_idx:])
        for row in reader:
            results.append(row)
    except Exception as e:
        log(f"Error reading buu_cuc_bat_on.csv: {e}")
    return results

# Define the Model Context Protocol (MCP) Tools Schema
TOOLS = [
    {
        "name": "get_am_list",
        "description": "Lists all Area Managers (AMs) in Nam Trung Bo region.",
        "inputSchema": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "name": "get_province_list",
        "description": "Lists all provinces in Nam Trung Bo region.",
        "inputSchema": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "name": "list_unstable_pos",
        "description": "Queries the list of unstable last-mile post offices (Bưu cục bất ổn) filtered optionally by AM name or Province.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "am_name": {"type": "string", "description": "Filter by Area Manager name (e.g. Trần Văn Phước)"},
                "province": {"type": "string", "description": "Filter by Province name (e.g. Đắk Nông)"}
            }
        }
    },
    {
        "name": "get_ops_kpi_summary",
        "description": "Calculates and returns aggregated KPI metrics (Total backlogs, aging ton, unstable PO counts) for a given AM, Province, or the whole region.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "am_name": {"type": "string", "description": "Filter by Area Manager name (e.g. Trần Văn Phước)"},
                "province": {"type": "string", "description": "Filter by Province name (e.g. Lâm Đồng)"}
            }
        }
    },
    {
        "name": "get_off_tuyen_spe",
        "description": "Returns the list of off-tuyến (off-duty) staff schedule details.",
        "inputSchema": {
            "type": "object",
            "properties": {}
        }
    }
]

def handle_request(req):
    method = req.get("method")
    params = req.get("params", {})
    req_id = req.get("id")

    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {}
                },
                "serverInfo": {
                    "name": "NTB-Ops-Assistant-MCP",
                    "version": "1.0.0"
                }
            }
        }
    elif method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": TOOLS
            }
        }
    elif method == "tools/call":
        tool_name = params.get("name")
        arguments = params.get("arguments", {})
        
        try:
            res_text = execute_tool(tool_name, arguments)
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": res_text
                        }
                    ]
                }
            }
        except Exception as e:
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {
                    "code": -32603,
                    "message": f"Internal error executing tool {tool_name}: {str(e)}"
                }
            }
    else:
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "error": {
                "code": -32601,
                "message": f"Method {method} not found"
            }
        }

def execute_tool(name, args):
    co_cau = read_co_cau()
    
    if name == "get_am_list":
        ams = sorted(list(set(item['am'] for item in co_cau.values() if item['am'])))
        return f"Area Managers (AMs) in Vùng Nam Trung Bộ:\n" + "\n".join(f"- {am}" for am in ams)

    elif name == "get_province_list":
        provinces = sorted(list(set(item['tinh'] for item in co_cau.values() if item['tinh'])))
        return f"Provinces in Vùng Nam Trung Bộ:\n" + "\n".join(f"- {p}" for p in provinces)

    elif name == "list_unstable_pos":
        am_name = args.get("am_name")
        province = args.get("province")
        
        unstable = read_unstable_pos()
        if not unstable:
            return "No unstable post offices found or buu_cuc_bat_on.csv is missing/empty."
            
        filtered = []
        for row in unstable:
            wh_id = row.get("kho_giao_id", "").strip()
            row_tinh = row.get("tinh_giao", "").strip()
            
            # Map AM from co_cau mapping
            row_am = co_cau.get(wh_id, {}).get("am", "") if wh_id in co_cau else ""
            if not row_am:
                # Try soft name matching if ID wasn't found
                row_name = row.get("kho_giao_name", "").strip()
                for item in co_cau.values():
                    if item['name'] in row_name or row_name in item['name']:
                        row_am = item['am']
                        break
            
            # Filter check
            if am_name and am_name.lower() not in row_am.lower():
                continue
            if province and province.lower() not in row_tinh.lower():
                continue
                
            filtered.append((row, row_am))

        if not filtered:
            return f"No unstable post offices found matching filters am_name={am_name}, province={province}."

        output = [f"Danh sách bưu cục bất ổn/cảnh báo (Bộ lọc: am={am_name or 'Tất cả'}, province={province or 'Tất cả'}):"]
        for row, ram in filtered:
            status = row.get("Trạng thái", "Bất ổn").strip()
            reasons = row.get("ly_do_bat_on", "N/A").strip()
            backlog_lm = row.get("bl lm", "N/A").strip()
            backlog_over5 = row.get("bl lm >5 ngay", "N/A").strip()
            clear_est = row.get("du_kien_clear_ton", "N/A").strip()
            name = row.get("kho_giao_name", "N/A").strip()
            tinh = row.get("tinh_giao", "N/A").strip()
            
            output.append(
                f"- Bưu cục: {name} (Tỉnh: {tinh} | AM: {ram})\n"
                f"  Trạng thái: {status} | Nguyên nhân: {reasons}\n"
                f"  Lượng đơn Backlog Last-Mile: {backlog_lm} đơn (Tồn >5 ngày: {backlog_over5} đơn)\n"
                f"  Dự kiến giải quyết tồn đọng: {clear_est} ngày\n"
            )
        return "\n".join(output)

    elif name == "get_ops_kpi_summary":
        am_name = args.get("am_name")
        province = args.get("province")
        
        unstable = read_unstable_pos()
        total_backlog_lm = 0
        total_backlog_over5 = 0
        unstable_count = 0
        warning_count = 0
        
        for row in unstable:
            wh_id = row.get("kho_giao_id", "").strip()
            row_tinh = row.get("tinh_giao", "").strip()
            row_am = co_cau.get(wh_id, {}).get("am", "") if wh_id in co_cau else ""
            
            if am_name and am_name.lower() not in row_am.lower():
                continue
            if province and province.lower() not in row_tinh.lower():
                continue
                
            try:
                total_backlog_lm += int(row.get("bl lm", "0").replace(',', '').strip())
            except ValueError:
                pass
            try:
                total_backlog_over5 += int(row.get("bl lm >5 ngay", "0").replace(',', '').strip())
            except ValueError:
                pass
            
            status = row.get("Trạng thái", "").strip()
            if status == "Bất ổn":
                unstable_count += 1
            elif status == "Cảnh báo" or "cảnh báo" in row.get("Trạng thái", "").lower():
                warning_count += 1
                
        target_desc = f"AM: {am_name}" if am_name else (f"Tỉnh: {province}" if province else "Toàn vùng Nam Trung Bộ")
        return (
            f"=== Báo Cáo Ops KPI Summary — {target_desc} ===\n"
            f"- Số bưu cục Bất ổn báo động: {unstable_count} bưu cục\n"
            f"- Số bưu cục Cảnh báo rủi ro: {warning_count} bưu cục\n"
            f"- Tổng đơn kẹt Last-Mile (Backlog): {total_backlog_lm} đơn\n"
            f"- Trong đó đơn kẹt > 5 ngày (Aging): {total_backlog_over5} đơn\n\n"
            f"Khuyến nghị: Xem chi tiết danh sách bưu cục bất ổn bằng công cụ 'list_unstable_pos' để điều phối SPE."
        )

    elif name == "get_off_tuyen_spe":
        if not os.path.exists('off_tuyen_spe.csv'):
            return "No off_tuyen_spe.csv file found."
        try:
            with open('off_tuyen_spe.csv', 'r', encoding='utf-8') as f:
                lines = f.readlines()
            if len(lines) < 2:
                return "off_tuyen_spe.csv is empty."
            return "Chi tiết lịch off-tuyến SPE:\n" + "".join(lines[1:])
        except Exception as e:
            return f"Error reading off_tuyen_spe.csv: {str(e)}"
            
    else:
        return f"Unknown tool: {name}"

def main():
    log("NTB Ops Assistant MCP Server started on stdio...")
    while True:
        try:
            line = sys.stdin.readline()
            if not line:
                break
            line = line.strip()
            if not line:
                continue
            
            req = json.loads(line)
            res = handle_request(req)
            
            # Write the response back to stdout
            sys.stdout.write(json.dumps(res) + "\n")
            sys.stdout.flush()
        except Exception as e:
            log(f"Error in MCP main loop: {e}")

if __name__ == "__main__":
    main()
