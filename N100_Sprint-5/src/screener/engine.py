import yaml
import pandas as pd


def load_config(path="config/screener_config.yaml"):
    with open(path, "r") as file:
        return yaml.safe_load(file)


def apply_filters(df, filters):
    result = df.copy()

    for key, value in filters.items():

        if key == "roe_min":
            result = result[result["roe_pct"] >= value]

        elif key == "debt_to_equity_max":
            result = result[
                (result["broad_sector"] == "Financials")
                | (result["debt_to_equity"] <= value)
            ]

        elif key == "free_cash_flow_min":
            result = result[result["free_cash_flow_cr"] >= value]

        elif key == "revenue_cagr_5y_min":
            result = result[result["revenue_cagr_5y"] >= value]

        elif key == "pat_cagr_5y_min":
            result = result[result["pat_cagr_5y"] >= value]

        elif key == "sales_min":
            result = result[result["sales"] >= value]
        elif key == "dividend_payout_max":
            result = result[result["dividend_payout_ratio_pct"] <= value]

        elif key == "pe_max":
            # Placeholder until P/E data is available
            pass

        elif key == "pb_max":
            # Placeholder until P/B data is available
            pass

        elif key == "dividend_yield_min":
            # Placeholder until Dividend Yield data is available
            pass

    return result