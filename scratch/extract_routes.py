with open("app.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

def find_range_of_route(route_str):
    for i, line in enumerate(lines):
        if route_str in line:
            # Found route, look for 'def ' below it
            for j in range(i+1, min(i+10, len(lines))):
                if lines[j].strip().startswith('def '):
                    func_name = lines[j].strip().split('(')[0].replace('def ', '')
                    # Find where the next def or route starts to estimate end line
                    end_idx = len(lines)
                    for k in range(j+1, len(lines)):
                        if lines[k].strip().startswith('@app.route') or (lines[k].strip().startswith('def ') and not lines[k].startswith('    ')):
                            end_idx = k
                            break
                    print(f"Route: {route_str} -> Function: {func_name} (Lines {j+1} to {end_idx})")
                    return j+1, end_idx
    print(f"Route {route_str} not found")
    return None

find_range_of_route("'/api/fd'")
find_range_of_route("'/api/operational'")
find_range_of_route("'/api/summary-dashboard'")
find_range_of_route("'/api/unstable-po'")
find_range_of_route("'/api/send-telegram-ai-briefing'")
