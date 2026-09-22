import docx
import html
import shutil
import os

docx_source = 'KICH_BAN_THUYET_TRINH_W38_INSIGHT_CHUYEN_SAU.docx'
doc = docx.Document(docx_source)

# Copy to all target docx files
targets = [
    'KICH_BAN_THUYET_TRINH_W38_NAM_TRUNG_BO.docx',
    'KICH_BAN_THUYET_TRINH_W38_INSIGHT_CHUYEN_SAU_CHINH_SUA.docx'
]
for t in targets:
    shutil.copyfile(docx_source, t)
    print(f"Copied to {t}")

html_parts = []
html_parts.append("""<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Kịch Bản Thuyết Trình Điều Hành W38 — Vùng Nam Trung Bộ</title>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Outfit:wght@600;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root {
            --bg-body: #f8fafc;
            --bg-card: #ffffff;
            --text-main: #0f172a;
            --text-muted: #64748b;
            --ghn-orange: #ea580c;
            --ghn-blue: #0f4c81;
            --success: #16a34a;
            --danger: #dc2626;
            --warning: #d97706;
            --border: #e2e8f0;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: 'Plus Jakarta Sans', sans-serif;
            background-color: var(--bg-body);
            color: var(--text-main);
            line-height: 1.6;
            padding: 24px;
        }
        .container {
            max-width: 1080px;
            margin: 0 auto;
            background: var(--bg-card);
            border-radius: 16px;
            box-shadow: 0 10px 25px -5px rgba(0,0,0,0.05);
            padding: 40px;
            border: 1px solid var(--border);
        }
        .header-box {
            text-align: center;
            border-bottom: 2px solid #e2e8f0;
            padding-bottom: 24px;
            margin-bottom: 32px;
        }
        .header-sub { font-size: 13px; font-weight: 700; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.5px; }
        .header-title { font-family: 'Outfit', sans-serif; font-size: 26px; font-weight: 800; color: var(--ghn-blue); margin: 8px 0; }
        .header-date { font-size: 14px; color: var(--text-muted); font-style: italic; }
        .header-tag { display: inline-block; background: #fff7ed; color: var(--ghn-orange); border: 1px solid #ffedd5; font-size: 12px; font-weight: 700; padding: 4px 12px; border-radius: 20px; margin-top: 10px; }
        
        .section-card {
            background: #ffffff;
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 24px;
            margin-bottom: 28px;
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.02);
        }
        .section-title {
            font-family: 'Outfit', sans-serif;
            font-size: 18px;
            font-weight: 700;
            color: var(--ghn-blue);
            margin-bottom: 16px;
            border-left: 4px solid var(--ghn-orange);
            padding-left: 12px;
        }
        .speech-heading {
            font-size: 14px;
            font-weight: 700;
            color: #b45309;
            background: #fef3c7;
            padding: 8px 14px;
            border-radius: 8px;
            margin-bottom: 14px;
            display: inline-block;
        }
        p { margin-bottom: 12px; font-size: 14.5px; }
        .bullet-point { margin-left: 20px; margin-bottom: 8px; font-size: 14.5px; }
        
        .callout {
            border-radius: 8px;
            padding: 12px 16px;
            margin: 12px 0;
            font-size: 13.5px;
        }
        .callout-insight { background: #eff6ff; border-left: 4px solid #3b82f6; color: #1e40af; }
        .callout-warning { background: #fef2f2; border-left: 4px solid #ef4444; color: #991b1b; }
        .callout-action { background: #f0fdf4; border-left: 4px solid #22c55e; color: #166534; }
        .callout-title { font-weight: 700; margin-bottom: 6px; display: flex; align-items: center; gap: 6px; }

        .top-btn {
            position: fixed;
            bottom: 24px;
            right: 24px;
            background: var(--ghn-orange);
            color: white;
            padding: 10px 18px;
            border-radius: 30px;
            text-decoration: none;
            font-weight: 700;
            font-size: 13px;
            box-shadow: 0 4px 12px rgba(234, 88, 12, 0.4);
        }
    </style>
</head>
<body>
    <div class="container">
""")

def process_paragraph(text, in_callout_type=None):
    text = text.strip()
    if not text:
        return None, in_callout_type
    
    # Headers
    if text.startswith("CÔNG TY CỔ PHẦN GIAO HÀNG NHANH"):
        return f'<div class="header-box"><div class="header-sub">{html.escape(text)}</div>', None
    if text.startswith("BÁO CÁO VẬN HÀNH & KINH DOANH TUẦN W38"):
        return f'<div class="header-title">{html.escape(text)}</div>', None
    if text.startswith("(Chu kỳ dữ liệu:"):
        return f'<div class="header-date">{html.escape(text)}</div>', None
    if text.startswith("KỊCH BẢN THUYẾT TRÌNH ĐIỀU HÀNH 16 CHUYÊN ĐỀ"):
        return f'<div class="header-tag">{html.escape(text)}</div></div>', None

    if any(text.startswith(icon + " [") for icon in ["📊", "📦", "🎯", "🔥", "📋", "⏱️", "🚚", "🌙", "🚨", "🔄", "🚛", "💰", "🛡️", "📈", "⚠️"]):
        return f'<div class="section-title">{html.escape(text)}</div>', None

    if text.startswith("🗣️"):
        return f'<div class="speech-heading">{html.escape(text)}</div>', None

    if "INSIGHT" in text and ("🔍" in text or "💡" in text):
        return f'<div class="callout callout-insight"><div class="callout-title"><i class="fa-solid fa-lightbulb"></i> {html.escape(text)}</div>', 'insight'
    if "CẢNH BÁO" in text and "⚠️" in text:
        return f'<div class="callout callout-warning"><div class="callout-title"><i class="fa-solid fa-triangle-exclamation"></i> {html.escape(text)}</div>', 'warning'
    if ("QUYẾT SÁCH" in text or "HÀNH ĐỘNG" in text) and ("🎯" in text or "⚡" in text):
        return f'<div class="callout callout-action"><div class="callout-title"><i class="fa-solid fa-crosshairs"></i> {html.escape(text)}</div>', 'action'
    
    if text.startswith("• ") or text.startswith("- ") or text.startswith("+ "):
        return f'<div class="bullet-point">{html.escape(text)}</div>', in_callout_type
    else:
        return f'<p>{html.escape(text)}</p>', in_callout_type

current_section_card = False
active_callout = None

for child in doc.element.body:
    if child.tag.endswith('p'):
        p = docx.text.paragraph.Paragraph(child, doc)
        text = p.text.strip()
        if not text:
            continue
        
        # Check if new section
        if any(text.startswith(icon + " [") for icon in ["📊", "📦", "🎯", "🔥", "📋", "⏱️", "🚚", "🌙", "🚨", "🔄", "🚛", "💰", "🛡️", "📈", "⚠️"]):
            if active_callout:
                html_parts.append('</div>')
                active_callout = None
            if current_section_card:
                html_parts.append('</div>')
            html_parts.append('<div class="section-card">')
            current_section_card = True

        frag, c_type = process_paragraph(text, active_callout)
        if frag:
            html_parts.append(frag)
            if c_type and c_type != active_callout:
                if active_callout:
                    html_parts.insert(len(html_parts)-1, '</div>')
                active_callout = c_type

    elif child.tag.endswith('tbl'):
        t = docx.table.Table(child, doc)
        for row in t.rows:
            for cell in row.cells:
                for p in cell.paragraphs:
                    text = p.text.strip()
                    if not text:
                        continue
                    
                    if "INSIGHT" in text and ("🔍" in text or "💡" in text):
                        if active_callout:
                            html_parts.append('</div>')
                        active_callout = 'insight'
                        frag = f'<div class="callout callout-insight"><div class="callout-title"><i class="fa-solid fa-lightbulb"></i> {html.escape(text)}</div>'
                        html_parts.append(frag)
                        continue
                    elif "CẢNH BÁO" in text and "⚠️" in text:
                        if active_callout:
                            html_parts.append('</div>')
                        active_callout = 'warning'
                        frag = f'<div class="callout callout-warning"><div class="callout-title"><i class="fa-solid fa-triangle-exclamation"></i> {html.escape(text)}</div>'
                        html_parts.append(frag)
                        continue
                    elif ("QUYẾT SÁCH" in text or "HÀNH ĐỘNG" in text) and ("🎯" in text or "⚡" in text):
                        if active_callout:
                            html_parts.append('</div>')
                        active_callout = 'action'
                        frag = f'<div class="callout callout-action"><div class="callout-title"><i class="fa-solid fa-crosshairs"></i> {html.escape(text)}</div>'
                        html_parts.append(frag)
                        continue

                    frag, _ = process_paragraph(text, active_callout)
                    if frag:
                        html_parts.append(frag)

        if active_callout:
            html_parts.append('</div>')
            active_callout = None

if active_callout:
    html_parts.append('</div>')
if current_section_card:
    html_parts.append('</div>')

html_parts.append("""
    </div>
    <a href="#" class="top-btn"><i class="fa-solid fa-arrow-up"></i> Về Đầu Trang</a>
</body>
</html>
""")

with open('KICH_BAN_THUYET_TRINH_W38_NAM_TRUNG_BO.html', 'w', encoding='utf-8') as f_html:
    f_html.write("\n".join(html_parts))

print("Successfully converted docx to KICH_BAN_THUYET_TRINH_W38_NAM_TRUNG_BO.html")
