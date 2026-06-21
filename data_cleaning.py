import pandas as pd
import sqlite3

df_nav = pd.read_csv("data/raw/02_nav_history.csv")
print(df_nav.head())

df_nav["date"] = pd.to_datetime(df_nav["date"])
print(df_nav.dtypes)

df_nav = df_nav.sort_values(by=["amfi_code", "date"])
print(df_nav.head(10))

df_nav = df_nav.drop_duplicates()
df_nav["nav"] = df_nav.groupby("amfi_code")["nav"].ffill()

print(df_nav.isnull().sum())
print(df_nav.shape)

df_nav.to_csv("data/processed/clean_nav_history.csv", index=False)


df_scheme = pd.read_csv("data/raw/07_scheme_performance.csv")
print(df_scheme.head())
print(df_scheme.isnull().sum())
print(df_scheme.dtypes)


conn = sqlite3.connect("bluestock_mf.db")
df_nav.to_sql("nav_history", conn, if_exists="replace", index=False)

print("done")


# SCHEME TABLE ADD

df_scheme.to_sql("scheme_performance", conn, if_exists="replace", index=False)
tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
print(tables)
query = "SELECT * FROM nav_history LIMIT 5"
print(pd.read_sql(query, conn))

df_trans = pd.read_csv("data/raw/08_investor_transactions.csv")

print(df_trans.head())
print(df_trans.columns)
print(df_trans.dtypes)


df_trans["transaction_date"] = pd.to_datetime(df_trans["transaction_date"])

print(df_trans["transaction_type"].unique())
print(df_trans["kyc_status"].unique())

print((df_trans["amount_inr"] <= 0).sum())

df_trans.to_csv(
    "data/processed/clean_investor_transactions.csv",
    index=False
)

df_trans.to_sql(
    "investor_transactions",
    conn,
    if_exists="replace",
    index=False
)

tables = conn.execute(
    "SELECT name FROM sqlite_master WHERE type='table';"
).fetchall()

print(tables)

print(len(df_nav))
print(len(df_scheme))
print(len(df_trans))