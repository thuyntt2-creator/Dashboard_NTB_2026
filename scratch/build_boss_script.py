# -*- coding: utf-8 -*-
import sys, os, json, docx
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

sys.stdout.reconfigure(encoding='utf-8')

# Load data
with open('data.json', 'r', encoding='utf-8') as f:
    db = json.load(f)

print('DB loaded successfully!')
