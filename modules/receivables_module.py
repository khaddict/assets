"""
This module handles the summary and total of receivables.
"""

from config import RECEIVABLES

def receivables_summary():
    """
    Return all receivables.
    """
    print("📄 Receivables".center(50))
    print("=" * 50)
    totals = {}

    for name, amount in RECEIVABLES:
        totals[name] = totals.get(name, 0) + amount

    for name, total in totals.items():
        print(f"📄 {name} owes you {total:.2f}€")

    overall_total = sum(totals.values())
    print(f"\n💰 Total Receivables: {overall_total:.2f}€")

def get_total_receivables():
    """
    Return the sum of all receivables.
    """
    return sum(amount for _, amount in RECEIVABLES)
