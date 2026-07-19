import pandas as pd
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SECTOR_FILE = (
    ROOT
    / "supporting_datasets"
    / "sectors.xlsx"
)
COMPANY_FILE = (
    ROOT
    / "datasets"
    / "companies.xlsx"
)

FINANCIAL_FILE = (
    ROOT
    / "supporting_datasets"
    / "financial_ratios.xlsx"
)


MARKET_FILE = (
    ROOT
    / "supporting_datasets"
    / "market_cap.xlsx"
)


OUTPUT_FOLDER = ROOT / "output"


OUTPUT_FOLDER.mkdir(
    exist_ok=True
)


print("Valuation Module Started 🚀")

financial = pd.read_excel(
    FINANCIAL_FILE,
    header=0
)


market = pd.read_excel(
    MARKET_FILE,
    header=0
)
sector = pd.read_excel(
    SECTOR_FILE,
    header=0
)


print("SECTOR COLUMNS:")
print(sector.columns.tolist())

print(sector.head())
# Convert financial year format

financial["year"] = (
    financial["year"]
    .astype(str)
    .str.extract(r'(\d{4})')
)


financial["year"] = pd.to_numeric(
    financial["year"],
    errors="coerce"
)


market["year"] = pd.to_numeric(
    market["year"],
    errors="coerce"
)

print(financial.head())
print("FINANCIAL COLUMNS:")
print(financial.columns.tolist())
print(market.head())
print("MARKET COLUMNS:")
print(market.columns.tolist())

# -------------------------
# Merge Financial + Market
# -------------------------

valuation_df = pd.merge(
    financial,
    market,
    on=[
        "company_id",
        "year"
    ],
    how="inner"
)


print("Merged Shape:")
print(valuation_df.shape)

# ===============================
# Sector Median P/E Calculation
# ===============================

valuation_df = valuation_df.merge(
    sector,
    on="company_id",
    how="left"
)
sector_pe = (
    valuation_df
    .groupby("broad_sector")["pe_ratio"]
    .median()
    .reset_index()
)

sector_pe.columns = [
    "broad_sector",
    "5yr_median_PE"
]


valuation_df = valuation_df.merge(
    sector_pe,
    on="broad_sector",
    how="left"
)


print("Sector Median PE Added ✅")
print(
    valuation_df[
        [
            "company_id",
            "broad_sector",
            "pe_ratio",
            "5yr_median_PE"
        ]
    ].head()
)


print(
    valuation_df.head()
)

# -------------------------
# FCF Yield Calculation
# -------------------------

valuation_df["FCF_yield_pct"] = (
    valuation_df["cash_from_operations_cr"]
    /
    valuation_df["market_cap_crore"]
) * 100


print(
    "FCF Yield Added ✅"
)


print(
    valuation_df[
        [
            "company_id",
            "year",
            "cash_from_operations_cr",
            "market_cap_crore",
            "FCF_yield_pct"
        ]
    ].head()
)

# -------------------------
# PE Comparison
# -------------------------

valuation_df["PE_vs_sector_median_pct"] = (
    (valuation_df["pe_ratio"] - valuation_df["5yr_median_PE"])
    /
    valuation_df["5yr_median_PE"]
) * 100


# -------------------------
# Valuation Flags
# -------------------------

def valuation_flag(row):

    if row["pe_ratio"] > row["5yr_median_PE"] * 1.5:
        return "Caution"

    elif row["pe_ratio"] < row["5yr_median_PE"] * 0.7:
        return "Discount"

    else:
        return "Fair"


valuation_df["flag"] = valuation_df.apply(
    valuation_flag,
    axis=1
)


print("PE Flag Added ✅")

print(
    valuation_df[
        [
            "company_id",
            "pe_ratio",
            "5yr_median_PE",
            "PE_vs_sector_median_pct",
            "flag"
        ]
    ].head()
)

# -------------------------
# Company Details Merge
# -------------------------

companies = pd.read_excel(
    COMPANY_FILE,
    header=1
)


companies = companies[
    [
        "id",
        "company_name"
    ]
]


companies = companies.rename(
    columns={
        "id":"company_id"
    }
)


valuation_df = valuation_df.merge(
    companies,
    on="company_id",
    how="left"
)


print("Company Name Added ✅")

print(
    valuation_df[
        [
            "company_id",
            "company_name"
        ]
    ].head()
)

# -------------------------
# Export Files
# -------------------------

final_columns = [
    "company_id",
    "company_name",
    "broad_sector",
    "pe_ratio",
    "pb_ratio",
    "ev_ebitda",
    "FCF_yield_pct",
    "5yr_median_PE",
    "PE_vs_sector_median_pct",
    "flag"
]


valuation_summary = valuation_df[
    final_columns
]


valuation_summary.to_excel(
    OUTPUT_FOLDER / "valuation_summary.xlsx",
    index=False
)


valuation_summary[
    valuation_summary["flag"]!="Fair"
].to_csv(
    OUTPUT_FOLDER / "valuation_flags.csv",
    index=False
)


print("Files Generated Successfully 🚀")