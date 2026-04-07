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
