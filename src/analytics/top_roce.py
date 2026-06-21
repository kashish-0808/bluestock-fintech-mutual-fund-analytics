import pandas as pd

df = pd.read_csv("data/processed/companies_clean.csv")

top10 = df.sort_values(
    by="roce_percentage",
    ascending=False
)[["company_name", "roce_percentage"]].head(10)

print(top10)