import pandas as pd

file_path = r"c:\Users\lap4all\Desktop\New folder\downloaded_user_sheet.xlsx"
df = pd.read_excel(file_path, sheet_name='dataGTC gốc full hàng')

print("Shape:", df.shape)
print("Duplicate rows count:", df.duplicated().sum())

# Let's group by Cấp Quản Lý, Chi tiết, Loại Hàng, Time and see if there are multiple entries
grouped = df.groupby(['Cấp Quản Lý', 'Chi tiết', 'Loại Hàng', 'Time']).size().reset_index(name='count')
duplicates = grouped[grouped['count'] > 1]
print("Duplicate key groups count:", len(duplicates))
if len(duplicates) > 0:
    print("Some examples:")
    print(duplicates.head())
