# -*- coding: utf-8 -*-
"""
Rebuild all presentation scripts with 100% accurate data for:
- Tab 1 Overview
- Tab 2-9
- Tab 10 (%FD Hoàn Trả - Full & TTS)
- Tab 11 (KTC & Vận Tải - 513 chuyến xe, 124 non tải 30%, 45.6% TLLĐ, 5.37h leadtime)
- Tab 12 (Aging tồn đọng 400 đơn & Treo luân chuyển 4.660 đơn - chuẩn AM và bưu cục Nam Trung Bộ)
- Tab 13-16
Generates DOCX, MD, and HTML files.
"""
import os, sys, json, re

sys.stdout.reconfigure(encoding='utf-8')
BASE_DIR = r"c:\Users\lap4all\Desktop\New folder"

# Load TOPICS from clean generator
from make_final_script import generate_md, generate_html, save_docx

# Let's inspect topics and make sure tab-10, tab-11, tab-12 are clean and correct!
