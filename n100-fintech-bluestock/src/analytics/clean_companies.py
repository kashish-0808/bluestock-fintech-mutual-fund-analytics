import pandas as pd

df = pd.read_csv("data/processed/companies.csv")

print("Before cleaning:", df.shape)

# fill missing numeric values with median
df["book_value"] = df["book_value"].fillna(df["book_value"].median())
df["roce_percentage"] = df["roce_percentage"].fillna(df["roce_percentage"].median())
df["roe_percentage"] = df["roe_percentage"].fillna(df["roe_percentage"].median())

# fill text missing values
df["website"] = df["website"].fillna("Not Available")

print("\nAfter cleaning nulls:", df.isnull().sum())

df.to_csv("data/processed/companies_clean.csv", index=False)

print("\nSaved cleaned file ✔️")