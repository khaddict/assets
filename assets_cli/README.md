# assets_cli - Terminal Dashboard 🖥️

Command-line interface for tracking personal finances including precious metals, crypto, cash, receivables, and stocks.

## Overview

Terminal-based dashboard that fetches real-time pricing data and displays portfolio summaries via interactive CLI menus.

## Features

- 💰 **Gold Portfolio**: Track investments, capital gains, taxes, net value
- 🥈 **Silver Portfolio**: Track investments, capital gains, taxes, net value
- 🪙 **Bitcoin Portfolio**: Strike-based BTC tracking with capital gains
- 📄 **Receivables**: Manage amounts owed to you
- 🏦 **Cash Overview**: Track cash balances across accounts
- 📉 **Stock Portfolio**: Tax calculations (holding duration: <5y vs ≥5y)
- 📈 **Portfolio Evolution**: Historical portfolio tracking
- 💬 **Discord Integration**: Send financial summaries via webhooks
- 📊 **Real-time Pricing**: Live gold, silver, BTC data from external APIs

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

## Configuration

Edit `config.py` with your portfolio data (see `config.py.template`).

**Optional**: Encrypt config with age

```bash
age -r age_key config.py -o config.py.age
age -d -i ~/.age/key.txt config.py.age > config.py
```

## Menu

```
==================================================
       🧭  Welcome to Your Assets Dashboard
==================================================
            What would you like to do?
==================================================
1. 💰 Gold Portfolio
2. 🥈 Silver Portfolio
3. 🪙 Bitcoin
4. 📄 Receivables
5. 🏦 Cash Overview
6. 📉 Stock Portfolio
7. 📊 Total Summary
8. 📈 Portfolio Evolution
9. 📤 Send Financial Summary
q. 🚪 Exit
```

## Alternative: Web Dashboard

For a web-based interface with SQLite persistence, admin tools, and Docker support, see [assets_gui](../assets_gui/).
3. 🪙 Bitcoin
4. 📄 Receivables
5. 🏦 Cash Overview
6. 📉 Stock Portfolio
7. 📊 Total Summary
8. 📈 Portfolio Evolution
9. 📤 Send Financial Summary
q. 🚪 Exit
==================================================
👉 Your choice: 4
==================================================
                  📄 Receivables
==================================================
📄 Toto owes you 150.00€
📄 Tata owes you 200.00€

💰 Total Receivables: 350.00€
==================================================
       🧭  Welcome to Your Assets Dashboard
==================================================
            What would you like to do?
==================================================
1. 💰 Gold Portfolio
2. 🥈 Silver Portfolio
3. 🪙 Bitcoin
4. 📄 Receivables
5. 🏦 Cash Overview
6. 📉 Stock Portfolio
7. 📊 Total Summary
8. 📈 Portfolio Evolution
9. 📤 Send Financial Summary
q. 🚪 Exit
==================================================
👉 Your choice: 5
==================================================
             🏦 Cash Holdings Summary
==================================================
🏠 Home Cash: 10.00€
🏦 Checking Account: 10.00€
📕 Livret A: 10.00€
🌱 LDDS: 10.00€
📘 BFM: 10.00€

🤑 Total Cash: 50.00€
==================================================
       🧭  Welcome to Your Assets Dashboard
==================================================
            What would you like to do?
==================================================
1. 💰 Gold Portfolio
2. 🥈 Silver Portfolio
3. 🪙 Bitcoin
4. 📄 Receivables
5. 🏦 Cash Overview
6. 📉 Stock Portfolio
7. 📊 Total Summary
8. 📈 Portfolio Evolution
9. 📤 Send Financial Summary
q. 🚪 Exit
==================================================
👉 Your choice: 6
==================================================
            📉 Stock Portfolio Summary
==================================================
💼 Initial investment: 1000.00€
📊 Current value: 1400.00€

🔍 Gain: 400.00€
🧾 Tax regime: Before 5 years (30%)
💸 Tax to pay: 120.00€

💵 Net value after tax: 1280.00€
==================================================
       🧭  Welcome to Your Assets Dashboard
==================================================
            What would you like to do?
==================================================
1. 💰 Gold Portfolio
2. 🥈 Silver Portfolio
3. 🪙 Bitcoin
4. 📄 Receivables
5. 🏦 Cash Overview
6. 📉 Stock Portfolio
7. 📊 Total Summary
8. 📈 Portfolio Evolution
9. 📤 Send Financial Summary
q. 🚪 Exit
==================================================
👉 Your choice: 7
==================================================
           📈 Overall Financial Summary
==================================================
💰 Gold: 16386.62€
🥈 Silver: 80.40€
📄 Receivables: 350.00€
🏦 Cash: 50.00€
📈 Stocks: 1280.00€
🔗 Bitcoin: 1247.77€

💼 Total Portfolio Value: 19394.79€
==================================================
       🧭  Welcome to Your Assets Dashboard
==================================================
            What would you like to do?
==================================================
1. 💰 Gold Portfolio
2. 🥈 Silver Portfolio
3. 🪙 Bitcoin
4. 📄 Receivables
5. 🏦 Cash Overview
6. 📉 Stock Portfolio
7. 📊 Total Summary
8. 📈 Portfolio Evolution
9. 📤 Send Financial Summary
q. 🚪 Exit
==================================================
👉 Your choice: 8
==================================================
==================================================
         📊 Portfolio Evolution Over Time
==================================================
Mar 2025 | █████████████ 11066.12 €
Apr 2025 | ████████████████████ 16077.21 €
==================================================
       🧭  Welcome to Your Assets Dashboard
==================================================
            What would you like to do?
==================================================
1. 💰 Gold Portfolio
2. 🥈 Silver Portfolio
3. 🪙 Bitcoin
4. 📄 Receivables
5. 🏦 Cash Overview
6. 📉 Stock Portfolio
7. 📊 Total Summary
8. 📈 Portfolio Evolution
9. 📤 Send Financial Summary
q. 🚪 Exit
==================================================
👉 Your choice: 9
==================================================
📈 Overall Financial Summary:
==================================================
✅ Message sent successfully!
==================================================
📊 Portfolio Evolution Over Time:
==================================================
✅ Message sent successfully!
==================================================
       🧭  Welcome to Your Assets Dashboard
==================================================
            What would you like to do?
==================================================
1. 💰 Gold Portfolio
2. 🥈 Silver Portfolio
3. 🪙 Bitcoin
4. 📄 Receivables
5. 🏦 Cash Overview
6. 📉 Stock Portfolio
7. 📊 Total Summary
8. 📈 Portfolio Evolution
9. 📤 Send Financial Summary
q. 🚪 Exit
==================================================
👉 Your choice: q
==================================================
👋 Goodbye! See you soon.
==================================================
```