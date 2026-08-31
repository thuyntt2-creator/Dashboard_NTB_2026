import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

transcript_path = r"C:\Users\lap4all\.gemini\antigravity-ide\brain\99fae90b-413f-4302-ba67-0dea689b73b1\.system_generated\logs\transcript.jsonl"

if os.path.exists(transcript_path):
    print("Found transcript file. Reading USER_INPUT messages:")
    with open(transcript_path, 'r', encoding='utf-8', errors='ignore') as f:
        for idx, line in enumerate(f, 1):
            try:
                data = json.loads(line)
                if data.get('type') == 'USER_INPUT':
                    content = data.get('content', '')
                    print(f"Step {data.get('step_index')}: {content}")
            except Exception as e:
                pass
else:
    print("Transcript not found.")
