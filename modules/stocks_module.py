from config import PEA_OPEN_DATE, INITIAL_INVESTMENT, CURRENT_VALUE, TAX_BEFORE_5Y, TAX_AFTER_5Y
from datetime import datetime

def is_after_five_years():
    today = datetime.today()
    delta = today - PEA_OPEN_DATE
    return delta.days >= 5 * 365

def compute_stock_taxes():
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
    _, _, net, _ = compute_stock_taxes()
    return net
