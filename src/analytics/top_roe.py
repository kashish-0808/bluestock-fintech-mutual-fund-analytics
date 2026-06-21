import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data/processed/companies_clean.csv")

top10 = df.sort_values(
    by="roe_percentage",
    ascending=False
).head(10)

plt.figure(figsize=(10,5))

plt.bar(
    top10["company_name"],
    top10["roe_percentage"]
)

plt.xticks(rotation=90)

plt.title("Top 10 Companies by ROE")
plt.ylabel("ROE (%)")

plt.tight_layout()

plt.show()