"""
Sprint 2 - Cash Flow KPI Engine

Day 11
Free Cash Flow
CFO Quality
CapEx Intensity
FCF Conversion
Capital Allocation
"""


def free_cash_flow(operating_activity, investing_activity):
    """
    Free Cash Flow (FCF)

    Formula:
    FCF = Operating Activity + Investing Activity

    Negative value is allowed.
    """

    return operating_activity + investing_activity

def cfo_quality_score(avg_cfo, avg_pat):
    """
    CFO Quality Score

    Formula:
    Average CFO / Average PAT
    """

    if avg_pat == 0:
        return None

    ratio = avg_cfo / avg_pat

    if ratio > 1.0:
        return "High Quality"

    elif ratio >= 0.5:
        return "Moderate"

    else:
        return "Accrual Risk"
    
def capex_intensity(investing_activity, sales):
    """
    CapEx Intensity

    Formula:
    abs(Investing Activity) / Sales × 100
    """

    if sales == 0:
        return None, None

    value = (abs(investing_activity) / sales) * 100

    if value < 3:
        label = "Asset Light"
    elif value <= 8:
        label = "Moderate"
    else:
        label = "Capital Intensive"

    return value, label




def fcf_conversion_rate(free_cash_flow, operating_profit):
    """
    FCF Conversion Rate

    Formula:
    (Free Cash Flow / Operating Profit) × 100
    """

    if operating_profit == 0:
        return None

    return (free_cash_flow / operating_profit) * 100


def capital_allocation_pattern(cfo, cfi, cff, cfo_pat_ratio=None):
    """
    Capital Allocation Pattern Classifier
    """

    cfo_sign = "+" if cfo >= 0 else "-"
    cfi_sign = "+" if cfi >= 0 else "-"
    cff_sign = "+" if cff >= 0 else "-"

    pattern = (cfo_sign, cfi_sign, cff_sign)

    if pattern == ("+", "-", "-"):
        if cfo_pat_ratio is not None and cfo_pat_ratio > 1:
            label = "Shareholder Returns"
        else:
            label = "Reinvestor"

    elif pattern == ("+", "+", "-"):
        label = "Liquidating Assets"

    elif pattern == ("-", "+", "+"):
        label = "Distress Signal"

    elif pattern == ("-", "-", "+"):
        label = "Growth Funded by Debt"

    elif pattern == ("+", "+", "+"):
        label = "Cash Accumulator"

    elif pattern == ("-", "-", "-"):
        label = "Pre-Revenue"

    elif pattern == ("+", "-", "+"):
        label = "Mixed"

    else:
        label = "Other"

    return cfo_sign, cfi_sign, cff_sign, label