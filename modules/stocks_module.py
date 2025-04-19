"""
This module handles the stock portfolio, including tax calculation and the display of the stock portfolio summary.
"""

from datetime import datetime
from config import PEA_OPEN_DATE, INITIAL_INVESTMENT, CURRENT_VALUE, TAX_BEFORE_5Y, TAX_AFTER_5Y

def is_after_five_years():
    """
    Checks if the PEA (Plan d'Épargne en Actions) investment is older than 5 years.
    Returns True if more than 5 years have passed since the PEA opened, otherwise False.
    """
    today = datetime.today()
    delta = today - PEA_OPEN_DATE
    return delta.days >= 5 * 365

def compute_stock_taxes():
    """
    Computes the stock portfolio tax, gain, and net value after tax.
    Takes into account whether the investment period is before or after 5 years to determine the applicable tax rate.
    """
    gain = max(0, CURRENT_VALUE - INITIAL_INVESTMENT)
    if is_after_five_years():
        tax_rate = TAX_AFTER_5Y
        regime = "After 5 years (17.2%)"
    else:
        tax_rate = TAX_BEFORE_5Y
        regime = "Before 5 years (30%)"

    tax = gain * tax_rate
    net = CURRENT_VALUE - tax
    return gain, tax, net, regime

def stocks_summary():
    """
    Displays a summary of the stock portfolio, including initial investment, current value, 
    gain, tax regime, tax to pay, and the net value after tax.
    """
    print("📉 Stock Portfolio Summary".center(50))
    print("=" * 50)
    print(f"💼 Initial investment: {INITIAL_INVESTMENT:.2f}€")
    print(f"📊 Current value: {CURRENT_VALUE:.2f}€")

    gain, tax, net, regime = compute_stock_taxes()

    print(f"\n🔍 Gain: {gain:.2f}€")
    print(f"🧾 Tax regime: {regime}")
    print(f"💸 Tax to pay: {tax:.2f}€")

    print(f"\n💵 Net value after tax: {net:.2f}€")

def get_total_stocks():
    """
    Returns the net value of the stock portfolio after tax.
    """
    _, _, net, _ = compute_stock_taxes()
    return net
