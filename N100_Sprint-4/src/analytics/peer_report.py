import pandas as pd


def create_peer_report(df, peer_groups, peer_percentiles):

    df = df.merge(
        peer_groups[
            [
                "company_id",
                "peer_group_name",
                "is_benchmark"
            ]
        ],
        on="company_id",
        how="left"
    )

    with pd.ExcelWriter(
        "output/peer_comparison.xlsx",
        engine="openpyxl"
    ) as writer:

        for group in sorted(
            df["peer_group_name"].dropna().unique()
        ):

            temp = df[
                df["peer_group_name"] == group
            ].copy()

            pivot = (
                peer_percentiles[
                    peer_percentiles["peer_group_name"] == group
                ]
                .pivot_table(
                    index=["company_id", "year"],
                    columns="metric",
                    values="percentile_rank"
                )
                .reset_index()
            )

            temp = temp.merge(
                pivot,
                on=["company_id", "year"],
                how="left"
            )

            temp.to_excel(
                writer,
                sheet_name=group[:31],
                index=False
            )

    print("✅ peer_comparison.xlsx created.")