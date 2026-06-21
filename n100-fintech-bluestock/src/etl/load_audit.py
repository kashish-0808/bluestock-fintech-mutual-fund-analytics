import pandas as pd
import os
from datetime import datetime
import sqlite3

DATA_PATH = "data/processed"
DB_PATH = "db/nifty100.db"

AUDIT_LOG = []

# -------------------------
# AUDIT FUNCTION
# -------------------------
def log_audit(table, file_name, rows, status, error=None):

    AUDIT_LOG.append({
        "table_name": table,
        "file_name": file_name,
        "rows_loaded": rows,
        "status": status,
        "error": error,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })


# -------------------------
# LOAD TO SQLITE + AUDIT
# -------------------------
def load_to_db(file_name, table_name, conn):

    try:
        path = os.path.join(DATA_PATH, file_name)
        df = pd.read_csv(path)

        df.to_sql(table_name, conn, if_exists="replace", index=False)

        print(f"✔ Loaded {table_name} ({len(df)} rows)")

        log_audit(table_name, file_name, len(df), "SUCCESS")

    except Exception as e:
        print(f"❌ Failed {table_name}: {str(e)}")

        log_audit(table_name, file_name, 0, "FAILED", str(e))


# -------------------------
# RUNNER
# -------------------------
def run_audit_loader():

    conn = sqlite3.connect(DB_PATH)

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
        load_to_db(file, table, conn)

    conn.close()

    # SAVE AUDIT FILE
    audit_df = pd.DataFrame(AUDIT_LOG)

    output_path = "data/processed/load_audit.csv"
    audit_df.to_csv(output_path, index=False)

    print("\n🚀 LOAD AUDIT COMPLETE")
    print("📄 Saved at:", output_path)
    print("\n📊 Total tables processed:", len(audit_df))


if __name__ == "__main__":
    run_audit_loader()