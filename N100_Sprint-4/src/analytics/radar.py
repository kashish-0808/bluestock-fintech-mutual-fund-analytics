import os
import numpy as np
import matplotlib.pyplot as plt


def generate_radar_charts(df):

    os.makedirs("reports/radar_charts", exist_ok=True)

    metrics = [
        "roe_pct",
        "roce_pct",
        "net_profit_margin_pct",
        "debt_to_equity",
        "free_cash_flow_cr",
        "pat_cagr_5y",
        "revenue_cagr_5y",
        "composite_quality_score"
    ]

    for company in df["company_id"].unique():

        temp = df[df["company_id"] == company]

        latest = temp.sort_values("year").iloc[-1]

        values = []

        for m in metrics:

            if m in latest.index:
                val = latest[m]
            else:
                val = 0

            if val is None:
                val = 0

            if np.isnan(val):
                val = 0

            values.append(float(val))

        values += values[:1]

        angles = np.linspace(
            0,
            2 * np.pi,
            len(metrics),
            endpoint=False
        ).tolist()

        angles += angles[:1]

        plt.figure(figsize=(6,6))

        ax = plt.subplot(111, polar=True)

        ax.plot(angles, values)

        ax.fill(angles, values, alpha=0.25)

        ax.set_xticks(angles[:-1])

        ax.set_xticklabels(metrics, fontsize=8)

        plt.title(company)

        plt.savefig(
            f"reports/radar_charts/{company}_radar.png",
            dpi=150,
            bbox_inches="tight"
        )

        plt.close()

    print("✅ Radar charts generated.")