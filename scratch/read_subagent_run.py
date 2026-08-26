import json

transcript_path = r"C:\Users\lap4all\.gemini\antigravity-ide\brain\a570b50e-300a-41ca-96a3-6b94e5e53638\.system_generated\logs\transcript.jsonl"

with open(transcript_path, 'r', encoding='utf-8') as f:
    for line in f:
        data = json.loads(line)
        # Check if this step has subagent output
        if data.get("type") == "BROWSER_SUBAGENT":
            content = data.get("content", "")
            print("=== SUBAGENT CONTENT ===")
            print(content[:2000])  # Print first 2000 chars of subagent report
            
            # Let's search for some strings in the content
            print("=== ERROR DETAILS IN SUBAGENT OUTPUT ===")
            if "See details" in content:
                print("Found 'See details' in subagent content.")
            if "error" in content.lower():
                print("Found 'error' in subagent content.")
