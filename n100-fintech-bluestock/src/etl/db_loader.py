import os
import pandas as pd
import sqlite3

DB_PATH = "db/nifty100.db"
DATA_PATH = "data/processed"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

def load_csv_to_table(file_name, table_name):
    file_path = os.path.join(DATA_PATH, file_name)
    
    df = pd.read_csv(file_path)

    print(f"\nLoading {file_name} → {table_name}")
    print("Rows:", df.shape[0])

    df.to_sql(table_name, conn, if_exists="replace", index=False)

    print(f"✔ Loaded into {table_name}")


if __name__ == "__main__":
    load_map = {
        "companies.csv": "companies",
        "profitandloss.csv": "profitandloss",
        "balancesheet.csv": "balancesheet",
        "cashflow.csv": "cashflow",
        "analysis.csv": "analysis",
        "documents.csv": "documents",
        "prosandcons.csv": "prosandcons"
    }

    for file, table in load_map.items():
        load_csv_to_table(file, table)

    conn.commit()
    conn.close()

    print("\n🚀 SQLite DB created successfully!")