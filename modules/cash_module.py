from config import ACCOUNTS

def cash_summary():
    print("🏦 Cash Holdings Summary".center(50))
    print("=" * 50)
    for label, amount in ACCOUNTS.items():
        print(f"{label}: {amount:.2f}€")
    total = get_total_cash()
    print(f"\n🤑 Total Cash: {total:.2f}€")

def get_total_cash():
    return sum(ACCOUNTS.values())
