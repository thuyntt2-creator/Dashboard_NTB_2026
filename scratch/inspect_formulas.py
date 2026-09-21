import gspread

gc = gspread.oauth(authorized_user_filename='authorized_user.json')
doc = gc.open_by_key('1E9BdaxouCeTUBeGLh0kyieyWE6wZoymglbZw19LRKEo')
ws = doc.worksheet('Tong quan T37')
cells = ['A2', 'B2', 'A3', 'B3', 'B10', 'C10', 'D10', 'B11', 'C11', 'D11', 'B13', 'C13', 'B19', 'C19', 'D19']
for c in cells:
    formula = ws.acell(c, value_render_option='FORMULA').value
    val = ws.acell(c).value
    print(f'{c}: formula="{formula}" | value="{val}"')
