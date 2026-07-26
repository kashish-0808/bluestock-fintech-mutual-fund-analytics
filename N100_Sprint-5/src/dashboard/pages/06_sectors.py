import streamlit as st
import plotly.express as px
from utils.db import get_valuation


st.title("🏭 Sector Analysis")


df = get_valuation()


sector = st.selectbox(
    "Select Sector",
    sorted(df["broad_sector"].dropna().unique())
)


sector_df = df[
    df["broad_sector"] == sector
]


st.subheader(
    f"{sector} Companies"
)


st.dataframe(
    sector_df[
        [
            "company_id",
            "pe_ratio",
            "FCF_yield_pct",
            "flag"
        ]
    ],
    use_container_width=True
)


# Sector chart

if "FCF_yield_pct" in sector_df.columns:

    fig = px.bar(
        sector_df,
        x="company_id",
        y="FCF_yield_pct",
        title="FCF Yield by Company"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )