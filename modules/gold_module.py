"""
Gold Portfolio Management: Handles price fetching, tax calculations, and net value computation 
for a gold portfolio using external product URLs and tax rates.
"""

from collections import defaultdict
from config import PRODUCT_URLS, GOLD_PORTFOLIO, FLAT_TAX_RATE, CAPITAL_GAIN_TAX_RATE
from bs4 import BeautifulSoup
import requests

def fetch_price(url):
    """
    Fetch the current price from a given product URL.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        price_element = soup.find(id="pv")
        if price_element:
            price_text = price_element.text.strip()
            clean_price = price_text.replace(' ', '').replace('€', '').replace(',', '.')
            return float(clean_price)
    except ImportError as e:
        print(f"Error fetching price ({url}): {e}")
    return None

def compute_taxes(buy_price, sell_price):
    """
    Compute taxes and net income based on purchase and sale price.
    """
    capital_gain = max(0, sell_price - buy_price)
    flat_tax = FLAT_TAX_RATE * sell_price
    capital_gain_tax = CAPITAL_GAIN_TAX_RATE * capital_gain
    tax = min(flat_tax, capital_gain_tax)
    regime = "capital gain" if tax == capital_gain_tax else "flat"
    net = sell_price - tax
    return capital_gain, flat_tax, capital_gain_tax, tax, regime, net

def display_gold_details(name, date_str, buy_price, sell_price, gain, flat_tax, gain_tax, tax, regime, net):
    """
    Print detailed gold asset information.
    """
    print(f"{name}")
    print(f"    - Purchase date: {date_str}")
    print(f"    - Purchase price: {buy_price:.2f}€")
    print(f"    - Sell price: {sell_price:.2f}€")
    print(f"    - Capital gain: {gain:.2f}€")
    print(f"    - Flat tax (11.5%): {flat_tax:.2f}€")
    print(f"    - Capital gain tax (36.2%): {gain_tax:.2f}€")
    print(f"    - Tax regime: {regime} (tax = {tax:.2f}€)")
    print(f"    💸 Net received: {net:.2f}€")

def get_total_net_gold(prices):
    """
    Calculate the total net value of all gold assets.
    """
    total_net = 0
    for name, _, buy_price in GOLD_PORTFOLIO:
        sell_price = prices.get(name)
        if sell_price:
            _, _, _, _, _, net = compute_taxes(buy_price, sell_price)
            total_net += net
    return total_net

def gold_summary():
    """
    Display a summary of the gold portfolio with per-asset and total values.
    """
    print("💰 Gold Portfolio Details".center(50))
    print("=" * 50)
    stats = defaultdict(lambda: {"gross": 0, "tax": 0, "net": 0, "count": 0})
    prices = {name: fetch_price(url) for name, url in PRODUCT_URLS.items()}

    for name, date_str, buy_price in GOLD_PORTFOLIO:
        sell_price = prices.get(name)
        if sell_price is None:
            print(f"❌ Sell price not available for: {name}\n")
            continue

        gain, flat_tax, gain_tax, tax, regime, net = compute_taxes(buy_price, sell_price)
        display_gold_details(
            name,
            date_str,
            buy_price,
            sell_price,
            gain,
            flat_tax,
            gain_tax,
            tax,
            regime,
            net
        )

        stat = stats[name]
        stat["gross"] += sell_price
        stat["tax"] += tax
        stat["net"] += net
        stat["count"] += 1

    print("=" * 50)
    print("💰 Gold Summary".center(50))
    print("=" * 50)
    for name, stat in stats.items():
        print(f"{name} ({stat['count']} units)")
        print(f"  - Total gross: {stat['gross']:.2f}€")
        print(f"  - Total tax: {stat['tax']:.2f}€")
        print(f"  💸 Net received: {stat['net']:.2f}€\n")

    total_net = get_total_net_gold(prices)
    print(f"💰 Net Gold Value: {total_net:.2f}€")
