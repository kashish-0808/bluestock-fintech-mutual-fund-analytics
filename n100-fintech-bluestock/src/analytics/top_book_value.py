import pandas as pd

df = pd.read_csv("data/processed/companies_clean.csv")

top10 = df.sort_values(
    by="book_value",
    ascending=False
)[["company_name", "book_value"]].head(10)

print(top10)