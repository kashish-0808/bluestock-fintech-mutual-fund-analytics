import streamlit as st
import plotly.express as px
from utils.db import get_valuation


st.title("📈 Trend Analysis")


df = get_valuation()


company = st.selectbox(
    "Select Company",
    sorted(df["company_id"].unique())
)


company_df = df[
    df["company_id"] == company
]


st.subheader(f"{company} Trend")


fig = px.line(
    company_df.reset_index(),
    x="index",
    y="pe_ratio",
    markers=True,
    title="P/E Ratio Trend"
)


st.plotly_chart(
    fig,
    use_container_width=True
)


st.dataframe(
    company_df,
    use_container_width=True
)