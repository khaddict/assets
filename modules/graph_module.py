from config import PORTFOLIO_EVOLUTION

def plot_graph(data: dict, title):
    if not data:
        print("❌ No data to display.")
        return

    print("=" * 50)
    print(f"{title}".center(50))
    print("=" * 50)

    max_label_length = max(len(str(label)) for label in data)
    max_value = max(data.values())
    scale = max_value / 40 if max_value > 0 else 1

    for label, value in data.items():
        bar = "█" * int(value / scale)
        print(f"{label.ljust(max_label_length)} | {bar} {value:.2f} €")

def show_portfolio_evolution():
    plot_graph(PORTFOLIO_EVOLUTION, title="📊 Portfolio Evolution Over Time")
