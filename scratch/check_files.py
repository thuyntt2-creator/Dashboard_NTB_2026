# -*- coding: utf-8 -*-
import openpyxl, os, sys, glob
import pandas as pd
sys.stdout.reconfigure(encoding='utf-8')

# Check files
print("Checking available excel files...")
for p in glob.glob(r'C:\Users\lap4all\Downloads\*.xlsx'):
    print("Download:", p)

for p in glob.glob(r'c:\Users\lap4all\Desktop\New folder\*.xlsx'):
    print("Project:", p)
