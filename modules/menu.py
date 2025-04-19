"""
This module provides the main menu for managing and displaying your financial portfolio.
"""

from modules.gold_module import gold_summary
from modules.receivables_module import receivables_summary
from modules.cash_module import cash_summary
from modules.stocks_module import stocks_summary
from modules.summary_module import overall_summary
from modules.graph_module import show_portfolio_evolution
from modules.send_financial_data import (
    send_overall_summary_to_discord,
    send_portfolio_evolution_to_discord
)

def print_title():
    """
    Prints the welcome title.
    """
    print("=" * 50)
    print("🧭  Welcome to Your Assets Dashboard".center(50))
    print("=" * 50)

def print_menu():
    """
    Prints the menu of available options.
    """
    print("What would you like to do?".center(50))
    print("=" * 50)
    print("1. 💰 Gold Portfolio")
    print("2. 📄 Receivables")
    print("3. 🏦 Cash Overview")
    print("4. 📉 Stock Portfolio")
    print("5. 📊 Total Summary")
    print("6. 📈 Portfolio Evolution")
    print("7. 📤 Send Financial Summary")
    print("q. 🚪 Exit")
    print("=" * 50)

def main_menu():
    """
    Main loop that displays the menu and handles user input.
    """
    while True:
        print_title()
        print_menu()
        choice = input("👉 Your choice: ").strip()

        if choice in ["1", "2", "3", "4", "5", "6", "7"]:
            print("=" * 50)

        if choice == "1":
            gold_summary()
        elif choice == "2":
            receivables_summary()
        elif choice == "3":
            cash_summary()
        elif choice == "4":
            stocks_summary()
        elif choice == "5":
            overall_summary()
        elif choice == "6":
            show_portfolio_evolution()
        elif choice == "7":
            print("📈 Overall Financial Summary:")
            print("=" * 50)
            send_overall_summary_to_discord()
            print("=" * 50)
            print("📊 Portfolio Evolution Over Time:")
            print("=" * 50)
            send_portfolio_evolution_to_discord()
        elif choice == "q":
            print("=" * 50)
            print("👋 Goodbye! See you soon.")
            print("=" * 50)
            break
        else:
            print("=" * 50)
            print("❌ Invalid choice. Please try again.")
