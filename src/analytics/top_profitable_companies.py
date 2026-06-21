import pandas as pd

companies = pd.read_csv("data/processed/companies_clean.csv")
profit = pd.read_csv("data/processed/profitandloss.csv")

latest_profit = profit[profit["year"] == "TTM"]

merged = pd.merge(
    companies,
    latest_profit,
    left_on="id",
    right_on="company_id",
    how="inner"
)

top10 = merged.sort_values(
    by="net_profit",
    ascending=False
)[["company_name", "net_profit"]].head(10)

print(top10)