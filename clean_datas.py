import pandas as pd

df = pd.read_csv('data/foot.csv')
df = df.drop_duplicates()
df = df.dropna(how='all')
cols_to_fill_zero = ['Gls', 'Ast', 'MP', 'Min']
df[cols_to_fill_zero] = df[cols_to_fill_zero].fillna(0)
df = df.dropna(subset=['Player', 'Nation'])
df['Player'] = df['Player'].str.strip()
df['Nation'] = df['Nation'].str.strip()
df['Pos'] = df['Pos'].str.strip()

if df['Min'].dtype == 'object':
    df['Min'] = pd.to_numeric(df['Min'].str.replace(',', ''), errors='coerce')
else:
    df['Min'] = pd.to_numeric(df['Min'], errors='coerce')

df['Gls'] = pd.to_numeric(df['Gls'], errors='coerce')
df['Ast'] = pd.to_numeric(df['Ast'], errors='coerce')
df['MP'] = pd.to_numeric(df['MP'], errors='coerce')

df.to_csv('data/foot-cleans.csv', index=False)
