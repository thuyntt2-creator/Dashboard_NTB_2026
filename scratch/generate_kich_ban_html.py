import re

with open('KICH_BAN_THUYET_TRINH_W37_NAM_TRUNG_BO.md', 'r', encoding='utf-8') as f:
    lines = f.readlines()

html_lines = []
in_blockquote = False
in_list = False

for line in lines:
    stripped = line.strip()
    
    # Headers
    if stripped.startswith('# '):
        html_lines.append(f"<h1>{stripped[2:]}</h1>")
        continue
    elif stripped.startswith('## '):
        if in_blockquote:
            html_lines.append("</blockquote>")
            in_blockquote = False
        if in_list:
            html_lines.append("</ul>")
            in_list = False
        html_lines.append(f"<h2>{stripped[3:]}</h2>")
        continue
    elif stripped.startswith('### '):
        html_lines.append(f"<h3>{stripped[4:]}</h3>")
        continue
    elif stripped.startswith('---'):
        if in_blockquote:
            html_lines.append("</blockquote>")
            in_blockquote = False
        if in_list:
            html_lines.append("</ul>")
            in_list = False
        html_lines.append("<hr>")
        continue
    
    if stripped == '>' or stripped == '> ':
        continue

    # Blockquote
    if stripped.startswith('> '):
        if not in_blockquote:
            html_lines.append("<blockquote>")
            in_blockquote = True
        content = stripped[2:].strip()
        if not content:
            continue
        # Convert markdown bold/italic
        content = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', content)
        content = re.sub(r'\*(.*?)\*', r'<em>\1</em>', content)
        if content.startswith('- '):
            html_lines.append(f"<p style='margin-left: 16px; margin-bottom: 6px;'>• {content[2:]}</p>")
        elif content == '':
            html_lines.append("<br>")
        else:
            html_lines.append(f"<p>{content}</p>")
        continue
    else:
        if in_blockquote:
            html_lines.append("</blockquote>")
            in_blockquote = False

    if stripped == '':
        if in_list:
            html_lines.append("</ul>")
            in_list = False
        continue

    # Regular line
    content = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', stripped)
    content = re.sub(r'\*(.*?)\*', r'<em>\1</em>', content)
    html_lines.append(f"<p>{content}</p>")

if in_blockquote:
    html_lines.append("</blockquote>")
if in_list:
    html_lines.append("</ul>")

body_content = "\n".join(html_lines)

full_html = f"""<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Kịch Bản Thuyết Trình Họp Tuần W37 - Vùng Nam Trung Bộ</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <style>
    :root {{
      --primary: #f97316;
      --primary-dark: #ea580c;
      --navy: #0f172a;
      --blue: #2563eb;
      --bg: #f8fafc;
      --surface: #ffffff;
      --text: #1e293b;
      --text-muted: #64748b;
      --border: #e2e8f0;
      --card-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.05);
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: 'Plus Jakarta Sans', sans-serif;
      background: var(--bg);
      color: var(--text);
      line-height: 1.7;
      padding: 24px;
      font-size: 15px;
    }}
    .container {{
      max-width: 1000px;
      margin: 0 auto;
      background: var(--surface);
      border-radius: 20px;
      padding: 40px;
      box-shadow: var(--card-shadow);
      border: 1px solid var(--border);
    }}
    .header-banner {{
      background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 100%);
      color: white;
      padding: 30px;
      border-radius: 16px;
      margin-bottom: 30px;
      text-align: center;
      position: relative;
    }}
    .header-banner h1 {{
      font-size: 22px;
      font-weight: 800;
      margin-bottom: 8px;
      letter-spacing: -0.5px;
      color: white;
    }}
    .header-banner p {{
      font-size: 14px;
      color: #94a3b8;
    }}
    .nav-actions {{
      display: flex;
      justify-content: center;
      gap: 12px;
      margin-top: 18px;
      flex-wrap: wrap;
    }}
    .btn {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      background: var(--primary);
      color: white;
      text-decoration: none;
      padding: 8px 18px;
      border-radius: 9999px;
      font-weight: 700;
      font-size: 13px;
      transition: all 0.2s ease;
    }}
    .btn:hover {{ background: var(--primary-dark); transform: translateY(-1px); }}
    .btn-secondary {{
      background: rgba(255, 255, 255, 0.15);
      border: 1px solid rgba(255, 255, 255, 0.2);
    }}
    .btn-secondary:hover {{ background: rgba(255, 255, 255, 0.25); }}

    h2 {{
      font-size: 18px;
      font-weight: 800;
      color: var(--navy);
      margin-top: 32px;
      margin-bottom: 16px;
      padding-bottom: 8px;
      border-bottom: 2px solid var(--border);
      display: flex;
      align-items: center;
      gap: 8px;
    }}
    blockquote {{
      background: #fff7ed;
      border-left: 4px solid var(--primary);
      padding: 18px 20px;
      border-radius: 0 12px 12px 0;
      margin: 16px 0 24px 0;
      font-style: normal;
      color: #334155;
    }}
    blockquote p {{ margin-bottom: 8px; }}
    blockquote p:last-child {{ margin-bottom: 0; }}
    strong {{ color: #0f172a; font-weight: 700; }}
    hr {{ border: none; border-top: 1px solid var(--border); margin: 30px 0; }}
  </style>
</head>
<body>
  <div class="container">
    <div class="header-banner">
      <span style="background: rgba(249, 115, 22, 0.2); color: #fb923c; padding: 4px 12px; border-radius: 9999px; font-size: 12px; font-weight: 800; text-transform: uppercase; margin-bottom: 10px; display: inline-block;">Chuẩn Số Liệu Thực Tế W37 (Đầy Đủ OPR TTS)</span>
      <h1>KỊCH BẢN THUYẾT TRÌNH BÁO CÁO HỌP TUẦN VẬN HÀNH & KINH DOANH W37</h1>
      <p>VÙNG NAM TRUNG BỘ — GHN EXPRESS (Kỳ báo cáo W37: 07/09/2026 - 13/09/2026)</p>
      <div class="nav-actions">
        <a href="http://127.0.0.1:3000/hop" class="btn" target="_blank">🖥️ Mở Dashboard W37</a>
        <a href="KICH_BAN_THUYET_TRINH_W37_NAM_TRUNG_BO_MOI_NHAT.docx" class="btn btn-secondary" download>📥 Tải File Word (.docx)</a>
      </div>
    </div>

    <div class="content">
      {body_content}
    </div>
  </div>
</body>
</html>
"""

with open('KICH_BAN_THUYET_TRINH_W37_NAM_TRUNG_BO.html', 'w', encoding='utf-8') as f:
    f.write(full_html)

print("SUCCESS: Generated KICH_BAN_THUYET_TRINH_W37_NAM_TRUNG_BO.html successfully!")
