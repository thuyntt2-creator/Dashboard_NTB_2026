import json

transcript_path = r"C:\Users\lap4all\.gemini\antigravity-ide\brain\a570b50e-300a-41ca-96a3-6b94e5e53638\.system_generated\logs\transcript.jsonl"

with open(transcript_path, 'r', encoding='utf-8') as f:
    for line in f:
        data = json.loads(line)
        if data.get("type") == "BROWSER_SUBAGENT":
            content = data.get("content", "")
            if "inspect_user_copy" in content or "CDB78271F0EBC0CFCF1EAE25AC2FC12B" in content:
                print("Found target subagent run!")
                # Let's save the entire content to a file to inspect it
                with open("scratch/subagent_run_details.txt", "w", encoding="utf-8") as out:
                    out.write(content)
                print("Saved to scratch/subagent_run_details.txt")
