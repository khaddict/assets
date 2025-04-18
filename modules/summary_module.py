from modules.gold_module import get_total_net_gold, PRODUCT_URLS, fetch_price
from modules.receivables_module import get_total_receivables
from modules.cash_module import get_total_cash
from modules.stocks_module import get_total_stocks

def overall_summary():
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
