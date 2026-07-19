import os
import pandas as pd


def generate_summary_report(df, output_folder="reports"):

    os.makedirs(output_folder, exist_ok=True)

    summary = {}

    summary["Total Companies"] = df["company_id"].nunique()

    summary["Total Records"] = len(df)

    summary["Average ROE"] = round(df["roe_pct"].mean(), 2)

    summary["Average ROCE"] = round(df["roce_pct"].mean(), 2)

    summary["Average Debt/Equity"] = round(
        df["debt_to_equity"].mean(), 2
    )

    summary["Average Composite Score"] = round(
        df["composite_quality_score"].mean(), 2
    )

    report = pd.DataFrame(
        summary.items(),
        columns=["Metric", "Value"]
    )

    report.to_excel(
        f"{output_folder}/summary_report.xlsx",
        index=False
    )

    return report