import json

transcript_path = r"C:\Users\lap4all\.gemini\antigravity-ide\brain\a570b50e-300a-41ca-96a3-6b94e5e53638\.system_generated\logs\transcript.jsonl"

with open(transcript_path, 'r', encoding='utf-8') as f:
    for i, line in enumerate(f):
        data = json.loads(line)
        if data.get("type") == "BROWSER_SUBAGENT":
            content = data.get("content", "")
            print(f"Index: {i}, length: {len(content)}, snippet: {content[:100]}...")
            with open(f"scratch/subagent_run_{i}.txt", "w", encoding="utf-8") as out:
                out.write(content)
