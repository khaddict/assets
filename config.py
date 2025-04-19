from datetime import datetime

# Discord webhook
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/123456789/abcdefghijklmnopqrstuvwxyz"

# Cash
ACCOUNTS = {
    "🏠 Home Cash": 100,
    "🏦 Checking Account": 200,
    "📘 Livret A": 1000,
    "🌱 LDDS": 500,
    "🏛️  BFM": 300
}

# Gold
PRODUCT_URLS = {
    "Gold Bar 100g 🪙": "https://www.achat-or-et-argent.fr/or/lingot-100g-or/3557",
    "Maple Leaf 🍁": "https://www.achat-or-et-argent.fr/or/maple-leaf-1-once-or/3192"
}

GOLD_PORTFOLIO = [
    ("Maple Leaf 🍁", "2023-06-20", 2000),
    ("Gold Bar 100g 🪙", "2025-04-07", 8000)
]

# Gold taxes
FLAT_TAX_RATE = 0.115
CAPITAL_GAIN_TAX_RATE = 0.362

# Stocks
PEA_OPEN_DATE = datetime(2025, 1, 1)
INITIAL_INVESTMENT = 1000.0
CURRENT_VALUE = 1400.0

# Stock taxes
TAX_BEFORE_5Y = 0.30
TAX_AFTER_5Y = 0.172

# Receivables
RECEIVABLES = [
    ("Rengar", 1000),
    ("Katarina", 500)
]

# Portfolio evolution
PORTFOLIO_EVOLUTION = {
    "Mar 2025": 11066.12,
    "Apr 2025": 16077.21
}
