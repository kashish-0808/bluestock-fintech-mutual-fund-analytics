import streamlit as st
from utils.db import get_valuation


st.title("🔎 Financial Screener")


df = get_valuation()


st.success(
    f"{len(df)} records loaded ✅"
)


st.sidebar.header("Filters")


pe_max = st.sidebar.slider(
    "Maximum P/E",
    0,
    100,
    50
)


fcf_min = st.sidebar.slider(
    "Minimum FCF Yield",
    0.0,
    10.0,
    0.0
)


filtered = df[
    (df["pe_ratio"] <= pe_max) &
    (df["FCF_yield_pct"] >= fcf_min)
]


st.subheader(
    f"{len(filtered)} companies match your filters"
)


show_columns = [
    "company_id",
    "company_name",
    "broad_sector",
    "pe_ratio",
    "FCF_yield_pct",
    "flag"
]


st.dataframe(
    filtered[show_columns],
    use_container_width=True
)


csv = filtered.to_csv(index=False)


st.download_button(
    "📥 Download CSV",
    csv,
    "screener_output.csv",
    "text/csv"
)