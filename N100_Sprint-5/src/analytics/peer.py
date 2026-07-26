import pandas as pd

def calculate_peer_percentiles(df, peer_groups):

    peer_groups = peer_groups[
        ["company_id", "peer_group_name", "is_benchmark"]
    ]

    df = df.merge(
        peer_groups,
        on="company_id",
        how="left",
        suffixes=("", "_peer")
    )

    metrics = [
        "roe_pct",
        "roce_pct",
        "net_profit_margin_pct",
        "debt_to_equity",
        "free_cash_flow_cr",
        "pat_cagr_5y",
        "revenue_cagr_5y",
        "eps_cagr_5y",
        "interest_coverage",
        "asset_turnover"
    ]

    records = []

    for group in df["peer_group_name"].dropna().unique():

        grp = df[df["peer_group_name"] == group]

        for metric in metrics:

            ranks = grp[metric].rank(pct=True)

            if metric == "debt_to_equity":
                ranks = 1 - ranks

            temp = grp[["company_id", "year"]].copy()
            temp["peer_group_name"] = group
            temp["metric"] = metric
            temp["value"] = grp[metric]
            temp["percentile_rank"] = ranks

            records.append(temp)

    return pd.concat(records, ignore_index=True)