import pandas as pd
from validator import run_dq_checks

DATA_PATH = "data/processed"

files = [
    "companies.csv",
    "profitandloss.csv",
    "balancesheet.csv",
    "cashflow.csv"
]

for file in files:
    df = pd.read_csv(f"{DATA_PATH}/{file}")
    run_dq_checks(df, file)