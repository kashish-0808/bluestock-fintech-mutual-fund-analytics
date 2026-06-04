-- Top 5 funds by AUM
SELECT amfi_code, aum_crore
FROM scheme_performance
ORDER BY aum_crore DESC
LIMIT 5;

-- Average NAV
SELECT AVG(nav) FROM nav_history;

-- NAV trend monthly
SELECT amfi_code, AVG(nav)
FROM nav_history
GROUP BY amfi_code;

-- Transactions by state
SELECT state, COUNT(*) 
FROM investor_transactions
GROUP BY state;

-- SIP vs Lumpsum count
SELECT transaction_type, COUNT(*)
FROM investor_transactions
GROUP BY transaction_type;

-- Expense ratio filter
SELECT amfi_code, expense_ratio_pct
FROM scheme_performance
WHERE expense_ratio_pct < 1;

-- High return funds
SELECT amfi_code, return_3yr_pct
FROM scheme_performance
ORDER BY return_3yr_pct DESC
LIMIT 5;

-- Risk distribution
SELECT risk_grade, COUNT(*)
FROM scheme_performance
GROUP BY risk_grade;

-- KYC status distribution
SELECT kyc_status, COUNT(*)
FROM investor_transactions
GROUP BY kyc_status;

-- Max NAV
SELECT MAX(nav) FROM nav_history;