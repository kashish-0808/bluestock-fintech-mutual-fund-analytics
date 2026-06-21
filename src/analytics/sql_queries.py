import sqlite3
import pandas as pd

DB_PATH = "db/nifty100.db"

conn = sqlite3.connect(DB_PATH)

# -----------------------------
# 1. TOP PROFIT COMPANIES
# -----------------------------
query1 = """
SELECT company_id, year, net_profit
FROM profitandloss
WHERE net_profit IS NOT NULL
ORDER BY net_profit DESC
LIMIT 10;
"""

top_profit = pd.read_sql(query1, conn)
print("\n🔥 TOP PROFIT COMPANIES")
print(top_profit)


# -----------------------------
# 2. TOP ROE COMPANIES
# -----------------------------
query2 = """
SELECT company_name, roe_percentage
FROM companies
ORDER BY roe_percentage DESC
LIMIT 10;
"""

top_roe = pd.read_sql(query2, conn)
print("\n🔥 TOP ROE COMPANIES")
print(top_roe)


# -----------------------------
# 3. TOP ROCE COMPANIES
# -----------------------------
query3 = """
SELECT company_name, roce_percentage
FROM companies
ORDER BY roce_percentage DESC
LIMIT 10;
"""

top_roce = pd.read_sql(query3, conn)
print("\n🔥 TOP ROCE COMPANIES")
print(top_roce)


# -----------------------------
# 4. HIGH VALUE COMPANIES
# -----------------------------
query4 = """
SELECT company_name, book_value
FROM companies
ORDER BY book_value DESC
LIMIT 10;
"""

top_book = pd.read_sql(query4, conn)
print("\n🔥 TOP BOOK VALUE COMPANIES")
print(top_book)


# -----------------------------
# CLOSE CONNECTION
# -----------------------------
conn.close()