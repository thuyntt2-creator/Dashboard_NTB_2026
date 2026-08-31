import json

transcript_path = r"C:\Users\lap4all\.gemini\antigravity-ide\brain\99fae90b-413f-4302-ba67-0dea689b73b1\.system_generated\logs\transcript.jsonl"

try:
    with open(transcript_path, 'r', encoding='utf-8') as f:
        for line in f:
            obj = json.loads(line)
            if "Console logs" in str(obj) or "console_logs" in str(obj) or "capture_browser_console_logs" in str(obj):
                # Print the tool result if available
                if obj.get("type") == "RUN_COMMAND" or obj.get("type") == "CONSOLE_LOGS_CAPTURE" or obj.get("type") == "PLANNER_RESPONSE":
                    pass
                else:
                    print(f"Step {obj.get('step_index')}: {obj.get('type')} / {obj.get('status')}")
                    print(json.dumps(obj, indent=2)[:2000])
                    print("="*80)
except Exception as e:
    print("Error:", str(e))
