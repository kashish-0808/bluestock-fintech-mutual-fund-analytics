import streamlit as st
from utils.db import get_valuation


st.title("📄 Annual Reports")


df = get_valuation()


company = st.selectbox(
    "Search Company",
    sorted(df["company_id"].unique())
)


st.subheader(
    f"Reports for {company}"
)


company_df = df[
    df["company_id"] == company
]


st.write(
    "📘 Annual Reports Available"
)

for i in range(1,6):
    st.write(
        f"📄 Annual Report {i}"
    )

    st.info(
        "Report link unavailable in dataset"
    )