"""
This module generates an overall financial summary of the user's portfolio,
combining the total values of gold, receivables, cash, and stocks. 
It fetches current gold prices, calculates the total net value of gold,
and adds the results of receivables, cash, and stocks to compute the overall portfolio value.
"""

from modules.gold_module import get_total_net_gold, PRODUCT_URLS, fetch_price
from modules.receivables_module import get_total_receivables
from modules.cash_module import get_total_cash
from modules.stocks_module import get_total_stocks

def overall_summary():
    """
    Displays the overall financial summary, including the total value of gold, receivables, 
    cash, and stocks. It fetches the current gold prices and computes the total portfolio value.
    """
    print("📈 Overall Financial Summary".center(50))
    print("=" * 50)

    prices = {name: fetch_price(url) for name, url in PRODUCT_URLS.items()}

    gold = get_total_net_gold(prices)
    receivables = get_total_receivables()
    cash = get_total_cash()
    stocks = get_total_stocks()

    total = gold + receivables + cash + stocks

    print(f"💰 Gold: {gold:.2f}€")
    print(f"📄 Receivables: {receivables:.2f}€")
    print(f"🏦 Cash: {cash:.2f}€")
    print(f"📈 Stocks: {stocks:.2f}€")
    print(f"\n💼 Total Portfolio Value: {total:.2f}€")
