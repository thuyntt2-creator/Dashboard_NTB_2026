import pandas as pd
import io
import urllib.request
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ss_id = '1DAwY-46twFrHIs77R4p4IMuIZ6JTE-e58Aj-9Kcr5Jk'

possible_sheets = [
    'Data', 'Datagtc', 'dataGTC gốc full hàng', 'dataGTC full hàng', 'dataGTC TTS',
    'DataLTC', 'Dataltc', 'dataLTC full hàng', 'dataLTC TTS', 'rawltc', 'Ca2', 'Ton',
    'Cơ cấu', 'cocau', 'Sheet1', 'Sheet2'
]

for sheet_name in possible_sheets:
    try:
        url = f'https://docs.google.com/spreadsheets/d/{ss_id}/gviz/tq?tqx=out:csv&sheet={urllib.parse.quote(sheet_name)}'
        df = pd.read_csv(url)
        print(f"Sheet '{sheet_name}' -> FOUND! Rows: {len(df)}, Cols: {len(df.columns)}")
        if 'Loại Hàng' in df.columns:
            print(f"  Loại Hàng unique: {df['Loại Hàng'].unique()[:5]}")
        elif 'Ca' in df.columns:
            print(f"  Ca unique: {df['Ca'].unique()[:5]}")
    except Exception as e:
        pass
