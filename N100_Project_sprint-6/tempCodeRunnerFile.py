"""SPRINT-3 """
from src.screener.engine import load_config, apply_filters
from src.screener.scoring import compute_composite_score
from src.analytics.peer import calculate_peer_percentiles
"""
Sprint 2 - Financial Ratio Engine
FINAL PRODUCTION VERSION
"""

import pandas as pd
import sqlite3

from src.analytics.ratios import *
from src.analytics.cagr import calculate_cagr
from src.analytics.cashflow_kpis import *


# =========================
# LOAD DATA
# =========================

# Main datasets
companies = pd.read_excel("datasets/companies.xlsx")
pl = pd.read_excel("datasets/profitandloss.xlsx", header=1)
bs = pd.read_excel("datasets/balancesheet.xlsx", header=1)
cf = pd.read_excel("datasets/cashflow.xlsx", header=1)
analysis = pd.read_excel("datasets/analysis.xlsx")
pros = pd.read_excel("datasets/prosandcons.xlsx")
documents = pd.read_excel("datasets/documents.xlsx")

# Supporting datasets
sec = pd.read_excel("supporting_datasets/sectors.xlsx")
peer = pd.read_excel("supporting_datasets/peer_groups.xlsx")
market_cap = pd.read_excel("supporting_datasets/market_cap.xlsx")
stock_prices = pd.read_excel("supporting_datasets/stock_prices.xlsx")
financial_ratios = pd.read_excel("supporting_datasets/financial_ratios.xlsx")


#temporary 
print("\nPeer Columns:")
print(peer.columns.tolist())


print("✅ All datasets loaded successfully.")


# =========================
# CLEAN FUNCTION
# =========================

def clean(df):
    df.columns = df.columns.str.strip().str.lower()

    possible = ["company_id", "company", "symbol", "ticker", "id"]

    col = None
    for c in possible:
        if c in df.columns:
            col = c
            break

    if col is None:
        raise ValueError("No company column found")

    df = df.rename(columns={col: "company_id"})
    df["company_id"] = df["company_id"].astype(str).str.upper().str.strip()
    return df


pl, bs, cf, sec = map(clean, [pl, bs, cf, sec])


# =========================
# CLEAN DUPLICATES
# =========================

cf = cf.drop_duplicates(["company_id", "year"])


# =========================
# MERGE
# =========================

df = pl.merge(bs, on=["company_id", "year"], how="inner")
df = df.merge(cf, on=["company_id", "year"], how="left")
df = df.merge(sec[["company_id", "broad_sector"]], on="company_id", how="left")

df = df[df["broad_sector"].notna()].copy()

print("\nFinal Shape:", df.shape)

print(df.columns.tolist())
# =========================
# RATIOS
# =========================

# Net Profit Margin
df["net_profit_margin_pct"] = df.apply(
    lambda r: net_profit_margin(r["net_profit"], r["sales"]),
    axis=1
)

# Operating Profit Margin
df["operating_profit_margin_pct"] = df.apply(
    lambda r: operating_profit_margin(
        r["operating_profit"],
        r["sales"]
    ),
    axis=1
)

# Return on Equity
df["roe_pct"] = df.apply(
    lambda r: return_on_equity(
        r["net_profit"],
        r["equity_capital"],
        r["reserves"]
    ),
    axis=1
)


# Return on Capital Employed
df["roce_pct"] = df.apply(
    lambda r: return_on_capital_employed(
        r["operating_profit"],
        r["equity_capital"],
        r["reserves"],
        r["borrowings"]
    ),
    axis=1
)

# Return on Assets
df["roa_pct"] = df.apply(
    lambda r: return_on_assets(
        r["net_profit"],
        r["total_assets"]
    ),
    axis=1
)

# Debt to Equity
df["debt_to_equity"] = df.apply(
    lambda r: debt_to_equity(
        r["borrowings"],
        r["equity_capital"],
        r["reserves"]
    ),
    axis=1
)

# Interest Coverage Ratio
df["interest_coverage"] = df.apply(
    lambda r: interest_coverage_ratio(
        r["operating_profit"],
        r["other_income"],
        r["interest"]
    ),
    axis=1
)

# Net Debt
df["net_debt"] = df.apply(
    lambda r: net_debt(
        r["borrowings"],
        r["investments"]
    ),
    axis=1
)

# Asset Turnover
df["asset_turnover"] = df.apply(
    lambda r: asset_turnover(
        r["sales"],
        r["total_assets"]
    ),
    axis=1
)

df["earnings_per_share"] = df["eps"]
df["total_debt_cr"] = df["borrowings"]
df["cash_from_operations_cr"] = df["operating_activity"]
df["book_value_per_share"] = df.apply(
    lambda r: None if r["equity_capital"] == 0
    else (r["equity_capital"] + r["reserves"]) / r["equity_capital"],
    axis=1
)
df["dividend_payout_ratio_pct"] = df["dividend_payout"]
df["capex_cr"] = abs(df["investing_activity"])

# Free Cash Flow
df["free_cash_flow_cr"] = df.apply(
    lambda r: free_cash_flow(
        r["operating_activity"],
        r["investing_activity"]
    ),
    axis=1
)

df["fcf_conversion_pct"] = df.apply(
    lambda r: fcf_conversion_rate(
        r["free_cash_flow_cr"],
        r["operating_profit"]
    ),
    axis=1
)


df["cfo_pat_ratio"] = df.apply(
    lambda r: None if r["net_profit"] == 0
    else r["operating_activity"] / r["net_profit"],
    axis=1
)
df["cfo_quality_score"] = df["cfo_pat_ratio"].apply(
    lambda x: cfo_quality_score(x, 1) if x is not None else None
)

patterns = df.apply(
    lambda r: capital_allocation_pattern(
        r["operating_activity"],
        r["investing_activity"],
        r["financing_activity"],
        r["cfo_pat_ratio"]
    ),
    axis=1
)
df["cfo_sign"] = patterns.apply(lambda x: x[0])
df["cfi_sign"] = patterns.apply(lambda x: x[1])
df["cff_sign"] = patterns.apply(lambda x: x[2])
df["pattern_label"] = patterns.apply(lambda x: x[3])


# CapEx Intensity
capex = df.apply(
    lambda r: capex_intensity(
        r["investing_activity"],
        r["sales"]
    ),
    axis=1
)

df["capex_pct"] = capex.apply(lambda x: x[0])
df["capex_label"] = capex.apply(lambda x: x[1])



# High Leverage Flag
df["high_leverage_flag"] = df.apply(
    lambda r: False if r["broad_sector"] == "Financials"
    else high_leverage_flag(
        r["debt_to_equity"],
        r["broad_sector"]
    ),
    axis=1
)

# Interest Coverage Labels & Warning
df["icr_label"] = df["interest_coverage"].apply(icr_label)
df["icr_warning"] = df["interest_coverage"].apply(icr_warning)


# =========================
# CAGR FIXED ENGINE
# =========================

def add_cagr(df, col, years, prefix):
    vals, flags = [], []

    for _, g in df.groupby("company_id"):
        g = g.sort_values("year")

        v = g[col].values

        for i in range(len(g)):
            if i < years - 1:
                vals.append(None)
                flags.append(None)
                continue

            start = v[i - (years - 1)]
            end = v[i]

            cagr_val, flag = calculate_cagr(start, end, years)

            vals.append(cagr_val)
            flags.append(flag)

    df[f"{prefix}_{years}y"] = vals
    df[f"{prefix}_{years}y_flag"] = flags


for y in [3, 5, 10]:
    add_cagr(df, "sales", y, "revenue_cagr")
    add_cagr(df, "net_profit", y, "pat_cagr")
    add_cagr(df, "eps", y, "eps_cagr")

# sprint-3
df = compute_composite_score(df)
import os

os.makedirs("output", exist_ok=True)

df[
    [
        "company_id",
        "year",
        "cfo_sign",
        "cfi_sign",
        "cff_sign",
        "pattern_label",
    ]
].to_csv(
    "output/capital_allocation.csv",
    index=False
)



# =========================
# SAVE DB
# =========================

conn = sqlite3.connect("database/financial_ratios.db")
df.to_sql("financial_ratios", conn, if_exists="replace", index=False)
conn.close()



import sqlite3

conn = sqlite3.connect("database/financial_ratios.db")

cursor = conn.cursor()
cursor.execute("SELECT COUNT(*) FROM financial_ratios")
print("Rows in DB:", cursor.fetchone()[0])

conn.close()
# =========================
# OUTPUT CHECK
# =========================

print("\nSample Output:")
print(df[[
    "company_id",
    "year",
    "net_profit_margin_pct",
    "roe_pct",
    "debt_to_equity",
    "interest_coverage",
    "icr_label",
    "icr_warning"
]].head(10))

print("\n✅ Sprint 2 Completed Successfully!")
print("Rows:", len(df))


print("\nTOP 5 CAPITAL PATTERNS:")
print(df[["company_id", "pattern_label"]].head())


# ---------- ADD HERE ----------
print("\nComposite Scores")
print(
    df[
        ["company_id", "composite_quality_score"]
    ].head()
)

"""SPRINT-3"""
config = load_config()

results = {}

for preset in config:

    result = apply_filters(df, config[preset])

    results[preset] = result

    print(f"\n===== {preset.upper()} =====")
    print(result[["company_id"]].head())
    print("Companies Found:", len(result))

    import os

os.makedirs("output", exist_ok=True)

with pd.ExcelWriter("output/screener_output.xlsx") as writer:

    for preset, result in results.items():
        result.to_excel(
            writer,
            sheet_name=preset[:31],   # Excel sheet name limit
            index=False
        )

print("\n✅ screener_output.xlsx created.")

peer_percentiles = calculate_peer_percentiles(df, peer)

print("\nPeer Percentiles")
print(peer_percentiles.head())

conn = sqlite3.connect("database/financial_ratios.db")

peer_percentiles.to_sql(
    "peer_percentiles",
    conn,
    if_exists="replace",
    index=False
)

conn.close()

print("✅ peer_percentiles table created.")