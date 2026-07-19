import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

import streamlit as st

st.title("🏢 Company Profile")

st.success("Profile Screen Loaded")

from utils.db import (
    get_company_data,
    get_companies,
)

st.set_page_config(
    page_title="Company Profile",
    page_icon="🏢",
    layout="wide"
)

# ----------------------------------------------------
# Load Company Master
# ----------------------------------------------------

COMPANY_FILE = (
    Path(__file__).resolve().parents[3]
    / "datasets"
    / "companies.xlsx"
)

companies = pd.read_excel(COMPANY_FILE, header=1)

st.title("🏢 Company Profile")

company_list = sorted(companies["id"].dropna().unique())

selected_company = st.selectbox(
    "Select Company",
    company_list
)

company_master = companies[
    companies["id"] == selected_company
].iloc[0]

financial_df = get_company_data(selected_company)

if financial_df.empty:
    st.error("Ticker not found. Please try another.")
    st.stop()

latest = financial_df.sort_values("year").iloc[-1]

# ----------------------------------------------------
# Company Card
# ----------------------------------------------------

left, right = st.columns([1,3])

with left:

    st.image(
        company_master["company_logo"],
        width=140
    )

with right:

    st.subheader(company_master["company_name"])

    st.write(company_master["about_company"])

    st.markdown(
        f"""
**Website**

{company_master["website"]}
"""
    )

    st.markdown(
        f"""
**NSE Profile**

{company_master["nse_profile"]}
"""
    )

# ----------------------------------------------------
# KPI Cards
# ----------------------------------------------------

st.divider()

c1,c2,c3 = st.columns(3)

c4,c5,c6 = st.columns(3)

c1.metric(
    "ROE",
    f"{latest['roe_pct']:.2f}%"
)

c2.metric(
    "ROCE",
    f"{latest['roce_pct']:.2f}%"
)

c3.metric(
    "Net Profit Margin",
    f"{latest['net_profit_margin_pct']:.2f}%"
)

c4.metric(
    "Debt / Equity",
    round(
        latest["debt_to_equity"],
        2
    )
)

c5.metric(
    "Revenue CAGR 5Y",
    f"{latest['revenue_cagr_5y']:.2f}%"
)

c6.metric(
    "Free Cash Flow",
    f"{latest['free_cash_flow_cr']:.2f} Cr"
)

st.divider()

# ----------------------------------------------------
# Revenue Chart
# ----------------------------------------------------

st.subheader("Revenue Trend")

fig = px.bar(
    financial_df,
    x="year",
    y="sales",
    text="sales"
)

fig.update_layout(
    height=450
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ----------------------------------------------------
# Net Profit Trend
# ----------------------------------------------------

st.subheader("Net Profit Trend")

fig = px.bar(
    financial_df,
    x="year",
    y="net_profit",
    text="net_profit"
)

fig.update_layout(height=450)

st.plotly_chart(
    fig,
    use_container_width=True
)



# ----------------------------------------------------
# ROE & ROCE Trend
# ----------------------------------------------------

st.subheader("ROE vs ROCE Trend")

trend_df = financial_df.sort_values("year")

fig = px.line(
    trend_df,
    x="year",
    y=["roe_pct", "roce_pct"],
    markers=True
)

fig.update_layout(
    height=450,
    xaxis_title="Year",
    yaxis_title="Percentage (%)",
    legend_title="Metrics"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ----------------------------------------------------
# Pros & Cons
# ----------------------------------------------------

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.subheader("✅ Pros")

    if latest["roe_pct"] >= 15:
        st.success("High Return on Equity")

    if latest["roce_pct"] >= 15:
        st.success("Strong Capital Efficiency")

    if latest["debt_to_equity"] < 1:
        st.success("Low Debt Company")

    if latest["free_cash_flow_cr"] > 0:
        st.success("Positive Free Cash Flow")

with col2:
    st.subheader("❌ Cons")

    if latest["debt_to_equity"] > 2:
        st.error("High Debt")

    if latest["net_profit_margin_pct"] < 5:
        st.error("Low Profit Margin")

    if latest["interest_coverage"] < 2:
        st.error("Weak Interest Coverage")

    if latest["free_cash_flow_cr"] < 0:
        st.error("Negative Free Cash Flow")