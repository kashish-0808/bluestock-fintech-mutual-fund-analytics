"""
CAGR Engine

Sprint 2 - Day 10
Revenue, PAT and EPS CAGR Calculations
"""


def calculate_cagr(start_value, end_value, years):
    """
    Calculate Compound Annual Growth Rate (CAGR).

    Formula:
    CAGR = ((End / Start) ** (1 / Years) - 1) * 100

    Returns:
        tuple: (cagr_value, flag)
    """

    # Less than required years
    if years <= 0:
        return None, "INSUFFICIENT"

    # Zero base
    if start_value == 0:
        return None, "ZERO_BASE"

    # Positive -> Negative
    if start_value > 0 and end_value < 0:
        return None, "DECLINE_TO_LOSS"

    # Negative -> Positive
    if start_value < 0 and end_value > 0:
        return None, "TURNAROUND"

    # Negative -> Negative
    if start_value < 0 and end_value < 0:
        return None, "BOTH_NEGATIVE"

    # Normal CAGR
    cagr = ((end_value / start_value) ** (1 / years) - 1) * 100

    return cagr, "NORMAL"

