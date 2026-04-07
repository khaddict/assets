"""
Bitcoin liquidation module (Strike-based approach).

This module:
- Uses the total fiat invested on Strike as the acquisition cost.
- Uses the current BTC balance on Strike to compute portfolio value.
- Fetches live BTC/EUR price from CoinGecko.
- Computes capital gain and net liquidation value using PFU (Flat Tax 30%).
"""

import requests
from config import STRIKE_TOTAL_INVESTED, STRIKE_CURRENT_BTC, BITCOIN_TAX_RATE


def fetch_btc_price():
    """
    Fetch the real-time BTC price in EUR from CoinGecko.
    """
    try:
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {"ids": "bitcoin", "vs_currencies": "eur"}
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return float(response.json()["bitcoin"]["eur"])
    except Exception as e:
        print(f"Error fetching BTC price: {e}")
        return None


def get_total_net_bitcoin():
    """
    Returns the net amount received if selling all BTC now.
    """
    if STRIKE_CURRENT_BTC <= 0:
        return 0.0

    price = fetch_btc_price()
    if price is None:
        return 0.0

    sale_value = STRIKE_CURRENT_BTC * price
    gain = sale_value - STRIKE_TOTAL_INVESTED
    taxable_gain = max(0.0, gain)
    tax = taxable_gain * BITCOIN_TAX_RATE
    net = sale_value - tax

    return net


def bitcoin_summary():
    """
    Display detailed summary for Bitcoin.
    """
    print("🔗 Bitcoin Summary".center(50))
    print("=" * 50)

    if STRIKE_CURRENT_BTC <= 0:
        print("No BTC currently held.")
        return

    price = fetch_btc_price()
    if price is None:
        print("⚠️ Could not fetch BTC price.")
        return

    sale_value = STRIKE_CURRENT_BTC * price
    gain = sale_value - STRIKE_TOTAL_INVESTED
    taxable_gain = max(0.0, gain)
    tax = taxable_gain * BITCOIN_TAX_RATE
    net = sale_value - tax

    print(f"BTC balance: {STRIKE_CURRENT_BTC:.8f} BTC")
    print(f"Total invested on Strike: {STRIKE_TOTAL_INVESTED:.2f}€")
    print(f"Current BTC price: {price:.2f}€")
    print(f"Gross liquidation value: {sale_value:.2f}€")
    print(f"Capital gain (taxable): {gain:.2f}€")
    print(f"Taxes (30% of {gain:.2f}): {tax:.2f}€")
    print(f"💸 Net if sold now: {net:.2f}€")
