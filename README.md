# Personal Finance Dashboard 💰

This project is a Python-based personal finance dashboard that allows you to track various financial aspects, such as gold portfolio, silver portfolio, receivables, cash holdings, stock investments, bitcoin, and overall portfolio evolution. It fetches real-time data for gold, silver and bitcoin prices and displays summaries, helping you stay up-to-date with your financial situation.

## Features

- **Gold Portfolio**: Tracks gold investments, calculates capital gains, tax, and net value.
- **Silver Portfolio**: Tracks silver investments, calculates capital gains, tax, and net value.
- **Receivables**: Displays a summary of the amounts owed to you by others.
- **Cash Holdings**: Overview of your current cash balances across various accounts.
- **Stock Portfolio**: Tracks stock investments, calculates taxes based on holding duration (before or after 5 years), and shows the net value after taxes.
- **Bitcoin Portfolio**: Tracks Bitcoin investments, calculates capital gains, tax, and net value.
- **Portfolio Evolution**: Plots the historical evolution of your overall portfolio.
- **Overall Summary**: Provides a total overview of all assets and liabilities, displaying the total portfolio value.
- **Send Financial Data to Discord**: Allows you to send financial summaries and portfolio data to a Discord channel via webhooks.
- **Dynamic Data Fetching**: Fetches real-time gold prices from external sources.

## Configuration

Modify the `config.py` static file.

OR USE AGE:

```bash
age -r age1w6g5qyw26h2708rc7xmc2nduywyw7mls0fj2h0rpmqtxv6r2mfsqvfj0h3 -o config.py.age config.py # encrypt
age -d -i ~/.age/key.txt config.py.age > config.py # decrypt
```

## Install

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

## Code

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
==================================================
👉 Your choice: 1
==================================================
             💰 Gold Portfolio Details
==================================================
Gold Maple Leaf 🍁
    - Purchase date: 2025-01-01
    - Purchase price: 3000.00€
    - Sell price: 3408.50€
    - Capital gain: 408.50€
    - Flat tax (11.5%): 391.98€
    - Capital gain tax (36.2%): 147.88€
    - Tax regime: capital gain (tax = 147.88€)
    💸 Net received: 3260.62€
Gold Bar 100g 💰
    - Purchase date: 2025-01-02
    - Purchase price: 8000.00€
    - Sell price: 10959.00€
    - Capital gain: 2959.00€
    - Flat tax (11.5%): 1260.29€
    - Capital gain tax (36.2%): 1071.16€
    - Tax regime: capital gain (tax = 1071.16€)
    💸 Net received: 9887.84€
Gold Bar 1oz 💰
    - Purchase date: 2025-01-03
    - Purchase price: 3000.50€
    - Sell price: 3373.00€
    - Capital gain: 372.50€
    - Flat tax (11.5%): 387.90€
    - Capital gain tax (36.2%): 134.84€
    - Tax regime: capital gain (tax = 134.84€)
    💸 Net received: 3238.16€
==================================================
                  💰 Gold Summary
==================================================
Gold Maple Leaf 🍁 (1 units)
  - Total gross: 3408.50€
  - Total tax: 147.88€
  💸 Net received: 3260.62€

Gold Bar 100g 💰 (1 units)
  - Total gross: 10959.00€
  - Total tax: 1071.16€
  💸 Net received: 9887.84€

Gold Bar 1oz 💰 (1 units)
  - Total gross: 3373.00€
  - Total tax: 134.84€
  💸 Net received: 3238.16€

💰 Net Gold Value: 16386.62€
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
👉 Your choice: 2
==================================================
            🥈 Silver Portfolio Details
==================================================
Silver Maple Leaf 🍁
    - Purchase date: 2025-01-01
    - Purchase price: 50.00€
    - Sell price: 40.20€
    - Capital gain: 0.00€
    - Flat tax (11.5%): 4.62€
    - Capital gain tax (36.2%): 0.00€
    - Tax regime: capital gain (tax = 0.00€)
    💸 Net received: 40.20€
Silver Maple Leaf 🍁
    - Purchase date: 2025-01-02
    - Purchase price: 50.00€
    - Sell price: 40.20€
    - Capital gain: 0.00€
    - Flat tax (11.5%): 4.62€
    - Capital gain tax (36.2%): 0.00€
    - Tax regime: capital gain (tax = 0.00€)
    💸 Net received: 40.20€
==================================================
                 🥈 Silver Summary
==================================================
Silver Maple Leaf 🍁 (2 units)
  - Total gross: 80.40€
  - Total tax: 0.00€
  💸 Net received: 80.40€

🥈 Net Silver Value: 80.40€
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
👉 Your choice: 3
==================================================
                🔗 Bitcoin Summary
==================================================
BTC balance: 0.01551969 BTC
Total invested on Strike: 2000.00€
Current BTC price: 80399.00€
Gross liquidation value: 1247.77€
Capital gain (taxable): -752.23€
Taxes (30% of -752.23): 0.00€
💸 Net if sold now: 1247.77€
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