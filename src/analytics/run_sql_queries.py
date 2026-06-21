import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DB_PATH = os.path.join(BASE_DIR, "..", "..", "db", "nifty100.db")
SQL_FILE = os.path.join(BASE_DIR, "..", "..", "notebooks", "exploratory_queries.sql")

conn = sqlite3.connect(DB_PATH)

with open(SQL_FILE, "r", encoding="utf-8") as f:
    sql_script = f.read()

queries = sql_script.split(";")

for q in queries:
    q = q.strip()
    if q:
        try:
            result = conn.execute(q).fetchall()
            print("\n======================")
            print(result[:5])
        except Exception as e:
            print("\n❌ Error:")
            print(q)
            print(e)

conn.close()