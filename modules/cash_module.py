"""
This module provides functions to display and calculate
summary information about cash accounts defined in the config.
"""

from config import ACCOUNTS

def cash_summary():
    """
    Display a summary of all cash holdings from the ACCOUNTS dictionary.
    Prints each account with its corresponding amount and calculates the total.
    """
    print("🏦 Cash Holdings Summary".center(50))
    print("=" * 50)
    for label, amount in ACCOUNTS.items():
        print(f"{label}: {amount:.2f}€")
    total = get_total_cash()
    print(f"\n🤑 Total Cash: {total:.2f}€")

def get_total_cash():
    """
    Calculate the total amount of cash from all accounts.
    """
    return sum(ACCOUNTS.values())
