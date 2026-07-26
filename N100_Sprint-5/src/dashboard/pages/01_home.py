import streamlit as st
from utils.db import get_valuation


st.title("🏠 Nifty 100 Analytics Dashboard")


df = get_valuation()


# KPI Cards

col1, col2, col3, col4 = st.columns(4)


col1.metric(
    "Total Companies",
    df["company_id"].nunique()
)


col2.metric(
    "Median P/E",
    round(df["pe_ratio"].median(), 2)
)


col3.metric(
    "Median FCF Yield",
    round(df["FCF_yield_pct"].median(), 2)
)


col4.metric(
    "Fair Value Stocks",
    len(df[df["flag"] == "Fair"])
)


st.divider()


st.subheader("📊 Valuation Overview")


st.dataframe(
    df.head(20),
    use_container_width=True
)