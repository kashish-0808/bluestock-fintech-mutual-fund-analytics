import streamlit as st
import pandas as pd
import sqlite3

DB_PATH = "db/nifty100.db"
conn = sqlite3.connect(DB_PATH)

st.set_page_config(page_title="N100 Dashboard", layout="wide")

st.title("📊 N100 Financial Intelligence Dashboard")
st.caption("ETL + SQL + Analytics powered system")

# Load data
companies = pd.read_sql("SELECT * FROM companies", conn)
profit = pd.read_sql("SELECT * FROM profitandloss", conn)

# =========================
# 🧠 INSIGHT SECTION (NEW)
# =========================
st.markdown("## 🧠 Key Insights")

top_roe = companies.loc[companies["roe_percentage"].idxmax()]
top_roce = companies.loc[companies["roce_percentage"].idxmax()]

col1, col2 = st.columns(2)

col1.success(f"🏆 Highest ROE: {top_roe['company_name']} ({top_roe['roe_percentage']})")
col2.success(f"🏆 Highest ROCE: {top_roce['company_name']} ({top_roce['roce_percentage']})")

# =========================
# FILTER
# =========================
st.sidebar.header("🔎 Filters")

company_list = companies["company_name"].dropna().unique()
selected_company = st.sidebar.selectbox("Select Company", company_list)

filtered = companies[companies["company_name"] == selected_company]

# =========================
# KPI METRICS
# =========================
col1, col2, col3 = st.columns(3)

col1.metric("Total Companies", len(companies))
col2.metric("Profit Records", len(profit))
col3.metric("Selected Company", selected_company)

# =========================
# COMPANY DETAILS
# =========================
st.subheader("🏢 Company Details")
st.dataframe(filtered)

# =========================
# TOP PROFIT
# =========================
st.subheader("💰 Top 10 Profitable Companies")

top_profit = (
    profit.groupby("company_id")["net_profit"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

st.bar_chart(top_profit)

# =========================
# ROE vs ROCE
# =========================
st.subheader("📈 ROE vs ROCE Comparison")

roe_roce = companies[["company_name", "roe_percentage", "roce_percentage"]].dropna()
roe_roce = roe_roce.set_index("company_name")

st.bar_chart(roe_roce)

# =========================
# PROFIT TREND (NEW WOW FEATURE)
# =========================
st.subheader("📉 Profit Trend (Top Companies)")

top_companies = (
    profit.groupby("company_id")["net_profit"]
    .sum()
    .sort_values(ascending=False)
    .head(5)
    .index
)

trend = profit[profit["company_id"].isin(top_companies)]

trend_chart = trend.pivot_table(
    index="year",
    columns="company_id",
    values="net_profit",
    aggfunc="sum"
)

st.line_chart(trend_chart)

# =========================
# RAW DATA
# =========================
with st.expander("📂 View Raw Data"):
    st.dataframe(companies)
    st.dataframe(profit)