import pandas as pd
import os

DATA_PATH = "data/processed"
OUTPUT_FILE = "data/processed/validation_failures.csv"

FAILURES = []

# -------------------------
# SMART RULES CONFIG
# -------------------------

NOT_ALLOWED_NEGATIVE = [
    "sales",
    "net_profit",
    "book_value",
    "roe_percentage",
    "roce_percentage"
]

ALLOWED_NEGATIVE = [
    "investing_activity",
    "financing_activity",
    "depreciation",
    "cwip",
    "interest"
]

# -------------------------
# CORE VALIDATION ENGINE
# -------------------------

def validate_dataset(df, file_name):

    print(f"\n🔍 Validating {file_name}")

    # -------------------------
    # RULE 1: NULL CHECK
    # -------------------------
    nulls = df.isnull().sum()

    for col, val in nulls.items():
        if val > 0:
            FAILURES.append({
                "file": file_name,
                "column": col,
                "issue": "NULL_VALUES",
                "count": int(val),
                "severity": "WARNING"
            })

    # -------------------------
    # RULE 2: DUPLICATES
    # -------------------------
    dup = df.duplicated().sum()

    if dup > 0:
        FAILURES.append({
            "file": file_name,
            "column": "ALL",
            "issue": "DUPLICATE_ROWS",
            "count": int(dup),
            "severity": "CRITICAL"
        })

    # -------------------------
    # RULE 3: NEGATIVE VALIDATION (SMART)
    # -------------------------
    numeric_cols = df.select_dtypes(include=["number"]).columns

    for col in numeric_cols:
        neg_count = (df[col] < 0).sum()

        if neg_count > 0:

            if col in NOT_ALLOWED_NEGATIVE:
                severity = "CRITICAL"
            else:
                severity = "INFO"

            FAILURES.append({
                "file": file_name,
                "column": col,
                "issue": "NEGATIVE_VALUES",
                "count": int(neg_count),
                "severity": severity
            })

    # -------------------------
    # RULE 4: BASIC FINANCIAL SANITY (EXAMPLE)
    # -------------------------
    if "sales" in df.columns and "net_profit" in df.columns:
        inconsistent = (df["net_profit"] > df["sales"]).sum()

        if inconsistent > 0:
            FAILURES.append({
                "file": file_name,
                "column": "net_profit",
                "issue": "PROFIT_GT_SALES",
                "count": int(inconsistent),
                "severity": "CRITICAL"
            })


# -------------------------
# RUNNER
# -------------------------

def run_all_checks():

    files = [
        "companies.csv",
        "profitandloss.csv",
        "balancesheet.csv",
        "cashflow.csv",
        "analysis.csv",
        "documents.csv",
        "prosandcons.csv"
    ]

    for file in files:
        path = os.path.join(DATA_PATH, file)

        df = pd.read_csv(path)
        validate_dataset(df, file)

    # -------------------------
    # SAVE REPORT
    # -------------------------
    report_df = pd.DataFrame(FAILURES)

    report_df.to_csv(OUTPUT_FILE, index=False)

    print("\n🚀 DQ VALIDATION COMPLETE")
    print("📄 Report saved at:", OUTPUT_FILE)
    print("\n🔥 CRITICAL ISSUES:", len(report_df[report_df['severity'] == 'CRITICAL']))


if __name__ == "__main__":
    run_all_checks()