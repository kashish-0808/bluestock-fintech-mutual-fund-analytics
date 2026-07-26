import pandas as pd

def compute_composite_score(df):
    df = df.copy()

    df["composite_quality_score"] = (
        df["roe_pct"].fillna(0) * 0.35 +
        df["roce_pct"].fillna(0) * 0.25 +
        df["net_profit_margin_pct"].fillna(0) * 0.15 +
        df["revenue_cagr_5y"].fillna(0) * 0.15 +
        (100 - df["debt_to_equity"].fillna(0)) * 0.10
    )

    return df