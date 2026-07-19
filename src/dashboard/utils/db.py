import sqlite3
from pathlib import Path

import pandas as pd
import streamlit as st

import streamlit as st
import pandas as pd
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]


@st.cache_data(ttl=600)
def load_excel(file):

    return pd.read_excel(
        ROOT / file
    )


@st.cache_data(ttl=600)
def get_valuation():

    return load_excel(
        "output/valuation_summary.xlsx"
    )


@st.cache_data(ttl=600)
def get_companies():

    return load_excel(
        "datasets/companies.xlsx"
    )


@st.cache_data(ttl=600)
def get_sectors():

    return load_excel(
        "supporting_datasets/sectors.xlsx"
    )

DB_PATH = Path(__file__).resolve().parents[3] / "database" / "financial_ratios.db"


@st.cache_data(ttl=600)
def get_data():
    """Load complete financial_ratios table"""
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql("SELECT * FROM financial_ratios", conn)
    conn.close()
    return df


@st.cache_data(ttl=600)
def get_latest_data():
    """Return latest year data"""
    df = get_data()
    latest_year = df["year"].max()
    return df[df["year"] == latest_year]


@st.cache_data(ttl=600)
def get_company_data(company_id):
    """Return all years data for one company"""
    df = get_data()
    return df[df["company_id"] == company_id]


@st.cache_data(ttl=600)
def get_companies():
    """Return sorted company list"""
    df = get_data()
    return sorted(df["company_id"].dropna().unique())


@st.cache_data(ttl=600)
def get_sectors():
    """Return all sectors"""
    df = get_data()
    return sorted(df["broad_sector"].dropna().unique())


@st.cache_data(ttl=600)
def get_sector_data(sector):
    """Return data for selected sector"""
    df = get_latest_data()
    return df[df["broad_sector"] == sector]


@st.cache_data(ttl=600)
def get_peer_data():
    """Load peer comparison table"""
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql("SELECT * FROM peer_percentiles", conn)
    conn.close()
    return df