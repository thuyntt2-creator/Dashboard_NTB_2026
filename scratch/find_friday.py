import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

path = r"C:\Users\lap4all\.gemini\antigravity-ide\brain\3c0e7a14-b7cd-479e-ac65-5a9c1303a7d0\.system_generated\logs\transcript_full.jsonl"
with open(path, "r", encoding="utf-8") as f:
    for line in f:
        item = json.loads(line)
        if item.get("step_index") in [903, 905, 907, 908]:
            idx = item.get("step_index")
            t = item.get("type")
            content = item.get("content", "")
            print(f"=== STEP {idx} ({t}) ===")
            print(content)
            print("\n" + "="*50 + "\n")
