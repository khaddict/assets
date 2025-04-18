import io
import sys
from modules.summary_module import overall_summary
from modules.graph_module import show_portfolio_evolution
from modules.discord_webhook import send_to_discord
from config import DISCORD_WEBHOOK_URL

def capture_output(func):
    output = io.StringIO()
    sys.stdout = output

    func()

    sys.stdout = sys.__stdout__

    return output.getvalue()

def send_overall_summary_to_discord():
    content = capture_output(overall_summary)
    send_to_discord(DISCORD_WEBHOOK_URL, content)

def send_portfolio_evolution_to_discord():
    content = capture_output(show_portfolio_evolution)
    send_to_discord(DISCORD_WEBHOOK_URL, content)
