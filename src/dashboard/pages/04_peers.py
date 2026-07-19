import streamlit as st
from utils.db import get_valuation
import plotly.express as px


st.title("👥 Peer Comparison")


df = get_valuation()


companies = sorted(
    df["company_id"].unique()
)


selected = st.selectbox(
    "Select Company",
    companies
)


company_df = df[
    df["company_id"] == selected
]


st.subheader(
    f"Comparison: {selected}"
)


st.dataframe(
    company_df.head(),
    use_container_width=True
)


# Simple metric comparison

metrics = [
    "pe_ratio",
    "pb_ratio",
    "ev_ebitda",
    "FCF_yield_pct"
]


chart_df = company_df[metrics].mean().reset_index()

chart_df.columns = [
    "Metric",
    "Value"
]


fig = px.bar(
    chart_df,
    x="Metric",
    y="Value",
    title="Valuation Metrics"
)


st.plotly_chart(
    fig,
    use_container_width=True
)