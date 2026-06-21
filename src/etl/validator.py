import pandas as pd

def run_dq_checks(df, name):
    print(f"\n🔍 Running DQ checks for {name}")

    issues = {}

    # 1. Null check
    issues["null_values"] = df.isnull().sum()

    # 2. Duplicate rows
    issues["duplicate_rows"] = df.duplicated().sum()

    # 3. Negative numeric check
    numeric_cols = df.select_dtypes(include=['number']).columns
    negative_counts = (df[numeric_cols] < 0).sum()
    issues["negative_values"] = negative_counts

    # Print summary
    print("\n--- NULLS ---")
    print(issues["null_values"])

    print("\n--- DUPLICATES ---")
    print(issues["duplicate_rows"])

    print("\n--- NEGATIVE VALUES ---")
    print(issues["negative_values"])

    return issues