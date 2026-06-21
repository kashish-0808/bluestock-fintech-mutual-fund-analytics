-- ================================
-- 1. TOP 10 PROFITABLE COMPANIES
-- ================================
SELECT company_id, year, net_profit
FROM profitandloss
ORDER BY net_profit DESC
LIMIT 10;


-- ================================
-- 2. TOP ROE COMPANIES
-- ================================
SELECT company_name, roe_percentage
FROM companies
ORDER BY roe_percentage DESC
LIMIT 10;


-- ================================
-- 3. TOP ROCE COMPANIES
-- ================================
SELECT company_name, roce_percentage
FROM companies
ORDER BY roce_percentage DESC
LIMIT 10;


-- ================================
-- 4. TOP BOOK VALUE COMPANIES
-- ================================
SELECT company_name, book_value
FROM companies
ORDER BY book_value DESC
LIMIT 10;


-- ================================
-- 5. AVERAGE PROFIT PER COMPANY
-- ================================
SELECT company_id, AVG(net_profit) AS avg_net_profit
FROM profitandloss
GROUP BY company_id
ORDER BY avg_net_profit DESC;


-- ================================
-- 6. PROFIT TREND (KEY COMPANIES)
-- ================================
SELECT company_id, year, net_profit
FROM profitandloss
WHERE company_id IN ('RELIANCE', 'TCS', 'HDFCBANK', 'SBIN')
ORDER BY company_id, year;


-- ================================
-- 7. HIGH ROE & ROCE FILTER
-- ================================
SELECT company_name, roe_percentage, roce_percentage
FROM companies
WHERE roe_percentage > 30 AND roce_percentage > 30
ORDER BY roe_percentage DESC;


-- ================================
-- 8. CASHFLOW HEALTH CHECK
-- ================================
SELECT company_id, operating_activity, investing_activity, financing_activity, net_cash_flow
FROM cashflow
ORDER BY net_cash_flow DESC;


-- ================================
-- 9. BALANCE SHEET STRENGTH
-- ================================
SELECT company_id, total_assets, total_liabilities
FROM balancesheet
ORDER BY total_assets DESC;


-- ================================
-- 10. RISK vs RETURN SNAPSHOT (JOIN)
-- ================================
SELECT 
    c.company_name,
    c.roe_percentage,
    p.net_profit
FROM companies c
JOIN profitandloss p
    ON c.id = p.company_id
WHERE p.year = 'TTM'
ORDER BY c.roe_percentage DESC;