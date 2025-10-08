import pandas as pd # type: ignore


na_values = ["N", "N/A", "NA", "--", "nan", "NaN", ""]

df = pd.read_csv('top5-players.csv', na_values=na_values)
print(df.head())

df = df.drop_duplicates()
df_clean = df.dropna()
df_clean = df_clean.reset_index(drop=True)

print(df_clean.head())

df_clean.to_csv('cleanplayer.csv', index=False)
