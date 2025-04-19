"""
Module for displaying portfolio evolution in a simple bar chart format.
"""

from config import PORTFOLIO_EVOLUTION

def plot_graph(data: dict, title: str):
    """
    Displays a bar chart for financial data in the CLI.
    """
    if not data:
        print("❌ No data to display.")
        return

    print("=" * 50)
    print(f"{title}".center(50))
    print("=" * 50)

    for label, value in data.items():
        bar = "█" * int(value / (max(data.values()) / 40))
        print(f"{label.ljust(max(len(str(label)) for label in data))} | {bar} {value:.2f} €")

def show_portfolio_evolution():
    """
    Displays the portfolio evolution using data from PORTFOLIO_EVOLUTION.
    """
    plot_graph(PORTFOLIO_EVOLUTION, title="📊 Portfolio Evolution Over Time")
