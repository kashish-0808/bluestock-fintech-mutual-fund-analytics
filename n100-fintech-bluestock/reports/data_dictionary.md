# Data Dictionary - Mutual Fund Analytics

## 1. nav_history
- amfi_code: Unique fund ID
- date: NAV date
- nav: Net Asset Value of fund

Business Use: Track fund performance over time

---

## 2. scheme_performance
- amfi_code: Fund ID
- scheme_name: Name of scheme
- fund_house: AMC name
- category: Fund type (Large Cap, Small Cap etc.)
- plan: Direct or Regular
- return_1yr_pct: 1 year return
- return_3yr_pct: 3 year return
- return_5yr_pct: 5 year return
- expense_ratio_pct: Fund cost percentage
- aum_crore: Assets under management

Business Use: Compare fund performance

---

## 3. investor_transactions
- investor_id: Unique investor ID
- transaction_date: Date of transaction
- amfi_code: Fund ID
- transaction_type: SIP / Lumpsum / Redemption
- amount_inr: Transaction amount
- state: Investor state
- city: Investor city
- city_tier: T30 / B30 classification
- kyc_status: Verified / Pending

Business Use: Investor behavior analysis

## Source Files

- nav_history → data/raw/02_nav_history.csv
- scheme_performance → data/raw/07_scheme_performance.csv
- investor_transactions → data/raw/08_investor_transactions.csv