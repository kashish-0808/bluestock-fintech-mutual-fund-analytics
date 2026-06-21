import pandas as pd

df = pd.read_csv("data/processed/profitandloss.csv")

top10 = df.sort_values(
    by="net_profit",
    ascending=False
)[["company_id", "year", "net_profit"]].head(10)

print(top10)