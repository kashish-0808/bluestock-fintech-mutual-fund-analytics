import streamlit as st
from utils.db import get_valuation
import plotly.express as px


st.title("💰 Capital Allocation Map")


df = get_valuation()


st.success("Capital Allocation Data Loaded ✅")


# Simple allocation based on valuation flag

capital_df = (
    df.groupby("flag")["company_id"]
    .nunique()
    .reset_index(name="Companies")
)


fig = px.treemap(
    capital_df,
    path=["flag"],
    values="Companies",
    title="Company Allocation Pattern"
)


st.plotly_chart(
    fig,
    use_container_width=True
)


st.subheader("Company List")


st.dataframe(
    df[
        [
            "company_id",
            "flag",
            "pe_ratio",
            "FCF_yield_pct"
        ]
    ],
    use_container_width=True
)