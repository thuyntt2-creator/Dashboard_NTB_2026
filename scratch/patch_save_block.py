# -*- coding: utf-8 -*-
with open('scratch/make_final_script.py', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace the save block
old_save_block = '''# Save DOCX files
target_docx = r"c:\\Users\\lap4all\\Desktop\\New folder\\KICH_BAN_THUYET_TRINH_W40_NAM_TRUNG_BO.docx"
doc.save(target_docx)
print(f"Saved workspace docx: {target_docx}")

# Copy to Downloads
downloads_docx_list = [
    r"C:\\Users\\lap4all\\Downloads\\KICH_BAN_W40_MOI_NHAT.docx",
    r"C:\\Users\\lap4all\\Downloads\\KICH_BAN_THUYET_TRINH_W40_CHUAN.docx"
]
for p in downloads_docx_list:
    try:
        shutil.copy2(target_docx, p)
        print(f"Copied docx to Downloads: {p}")
    except Exception as e:
        print(f"Warning: Could not copy to {p}: {e}")

# Attempt to copy to locked user file if not locked
try:
    shutil.copy2(target_docx, r"C:\\Users\\lap4all\\Downloads\\kịch bản.docx")
    print("Successfully overwritten C:\\\\Users\\\\lap4all\\\\Downloads\\\\kịch bản.docx")
except Exception as e:
    print(f"Notice: C:\\\\Users\\\\lap4all\\\\Downloads\\\\kịch bản.docx is currently open in Word: {e}")'''

new_save_block = '''# Save DOCX files with lock handling
target_docx = r"c:\\Users\\lap4all\\Desktop\\New folder\\KICH_BAN_THUYET_TRINH_W40_NAM_TRUNG_BO.docx"
saved_src = None

# Save to Downloads first (where KICH_BAN_W40_MOI_NHAT.docx is usually not locked)
dl_main = r"C:\\Users\\lap4all\\Downloads\\KICH_BAN_W40_MOI_NHAT.docx"
try:
    doc.save(dl_main)
    saved_src = dl_main
    print(f"Saved docx to Downloads: {dl_main}")
except Exception as e:
    print(f"Notice: Could not save to {dl_main}: {e}")

# Save to workspace target
try:
    doc.save(target_docx)
    saved_src = target_docx
    print(f"Saved workspace docx: {target_docx}")
except Exception as e:
    fallback_ws = r"c:\\Users\\lap4all\\Desktop\\New folder\\KICH_BAN_THUYET_TRINH_W40_MOI.docx"
    doc.save(fallback_ws)
    if not saved_src:
        saved_src = fallback_ws
    print(f"Notice: {target_docx} is open in Word, saved to fallback: {fallback_ws}")

# Also save to CHUAN in Downloads
try:
    doc.save(r"C:\\Users\\lap4all\\Downloads\\KICH_BAN_THUYET_TRINH_W40_CHUAN.docx")
    print("Saved docx to C:\\Users\\lap4all\\Downloads\\KICH_BAN_THUYET_TRINH_W40_CHUAN.docx")
except Exception as e:
    print(f"Notice: Could not save to KICH_BAN_THUYET_TRINH_W40_CHUAN.docx: {e}")

# Try to save to kịch bản.docx if closed
try:
    doc.save(r"C:\\Users\\lap4all\\Downloads\\kịch bản.docx")
    print("Successfully updated C:\\Users\\lap4all\\Downloads\\kịch bản.docx")
except Exception as e:
    print(f"Notice: C:\\Users\\lap4all\\Downloads\\kịch bản.docx is open in Word: {e}")'''

if old_save_block in text:
    text = text.replace(old_save_block, new_save_block)
    with open('scratch/make_final_script.py', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Replaced save block successfully!")
else:
    print("Warning: old_save_block not exact match, check lines.")
