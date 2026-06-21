import pandas as pd

df = pd.read_csv("data/processed/companies.csv")

print("SHAPE:", df.shape)
print("\nCOLUMNS:", df.columns)
print("\nNULL VALUES:\n", df.isnull().sum())

print("\nTOP 5 ROWS:")
print(df.head())