"""
Financial Ratio Engine

Sprint 2 - Day 8
Profitability, Leverage & Efficiency Ratios
"""

import pandas as pd

# ==========================================
# Profitability Ratios
# ==========================================

def net_profit_margin(net_profit, sales):
    """
    Net Profit Margin = (Net Profit / Sales) × 100

    Returns:
        float : Net Profit Margin (%)
        None  : If sales is 0
    """
    if sales == 0:
        return None

    return (net_profit / sales) * 100


def operating_profit_margin(operating_profit, sales):
    """
    Operating Profit Margin = (Operating Profit / Sales) × 100

    Returns:
        float : Operating Profit Margin (%)
        None  : If sales is 0
    """
    if sales == 0:
        return None

    return (operating_profit / sales) * 100


def return_on_equity(net_profit, equity_capital, reserves):
    """
    Return on Equity (ROE)
    = (Net Profit / (Equity Capital + Reserves)) × 100
    """
    total_equity = equity_capital + reserves

    if total_equity <= 0:
        return None

    return (net_profit / total_equity) * 100


def return_on_capital_employed(ebit, equity_capital, reserves, borrowings):
    """
    Return on Capital Employed (ROCE)
    = (EBIT / (Equity + Reserves + Borrowings)) × 100
    """
    capital_employed = equity_capital + reserves + borrowings

    if capital_employed <= 0:
        return None

    return (ebit / capital_employed) * 100


def return_on_assets(net_profit, total_assets):
    """
    Return on Assets (ROA)
    = (Net Profit / Total Assets) × 100
    """
    if total_assets == 0:
        return None

    return (net_profit / total_assets) * 100


# ==========================================
# Leverage Ratios
# ==========================================

def debt_to_equity(borrowings, equity_capital, reserves):
    """
    Debt to Equity
    = Borrowings / (Equity + Reserves)

    Returns:
        0     : If borrowings = 0
        None  : If Equity + Reserves <= 0
    """
    if borrowings == 0:
        return 0

    total_equity = equity_capital + reserves

    if total_equity <= 0:
        return None

    return borrowings / total_equity


def interest_coverage_ratio(operating_profit, other_income, interest):
    """
    Interest Coverage Ratio (ICR)
    = (Operating Profit + Other Income) / Interest
    """
    if interest == 0:
        return None

    return (operating_profit + other_income) / interest


def net_debt(borrowings, investments):
    """
    Net Debt = Borrowings - Investments
    """
    return borrowings - investments


def asset_turnover(sales, total_assets):
    """
    Asset Turnover = Sales / Total Assets
    """
    if total_assets == 0:
        return None

    return sales / total_assets


# ==========================================
# Flags & Labels
# ==========================================

def high_leverage_flag(debt_to_equity, broad_sector):
    """
    Returns True if Debt-to-Equity > 5 and company
    is not in Financials sector.
    """

    if pd.isna(debt_to_equity):
        return False

    if broad_sector == "Financials":
        return False

    return debt_to_equity > 5


def icr_label(interest_coverage):
    """
    Returns display label for Interest Coverage Ratio.
    """

    if pd.isna(interest_coverage):
        return "Debt Free"

    return ""


def icr_warning(interest_coverage):
    """
    Returns True if Interest Coverage Ratio is below 1.5.
    """

    if pd.isna(interest_coverage):
        return False

    return interest_coverage < 1.5

