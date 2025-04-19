# Personal Finance Dashboard 💰

This project is a Python-based personal finance dashboard that allows you to track various financial aspects, such as gold portfolio, receivables, cash holdings, stock investments, and overall portfolio evolution. It fetches real-time data for gold prices and displays summaries, helping you stay up-to-date with your financial situation.

## Features

- **Gold Portfolio**: Tracks gold investments, calculates capital gains, tax, and net value.
- **Receivables**: Displays a summary of the amounts owed to you by others.
- **Cash Holdings**: Overview of your current cash balances across various accounts.
- **Stock Portfolio**: Tracks stock investments, calculates taxes based on holding duration (before or after 5 years), and shows the net value after taxes.
- **Portfolio Evolution**: Plots the historical evolution of your overall portfolio.
- **Overall Summary**: Provides a total overview of all assets and liabilities, displaying the total portfolio value.
- **Send Financial Data to Discord**: Allows you to send financial summaries and portfolio data to a Discord channel via webhooks.
- **Dynamic Data Fetching**: Fetches real-time gold prices from external sources.

## Configuration

Modify the `config.py` static file.

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
1. 🪙 Gold Portfolio
2. 📄 Receivables
3. 🏦 Cash Overview
4. 📉 Stock Portfolio
5. 📊 Total Summary
6. 📈 Portfolio Evolution
7. 📤 Send Financial Summary
q. 🚪 Exit
==================================================
👉 Your choice: 1
==================================================
            🪙 Gold Portfolio Details             
==================================================
Maple Leaf 🍁
    - Purchase date: 2023-06-20
    - Purchase price: 2000.00€
    - Sell price: 2840.00€
    - Capital gain: 840.00€
    - Flat tax (11.5%): 326.60€
    - Capital gain tax (36.2%): 304.08€
    - Tax regime: capital gain (tax = 304.08€)
    💸 Net received: 2535.92€
Gold Bar 100g 🪙
    - Purchase date: 2025-04-07
    - Purchase price: 8000.00€
    - Sell price: 9036.50€
    - Capital gain: 1036.50€
    - Flat tax (11.5%): 1039.20€
    - Capital gain tax (36.2%): 375.21€
    - Tax regime: capital gain (tax = 375.21€)
    💸 Net received: 8661.29€
==================================================
                 🪙 Gold Summary                  
==================================================
Maple Leaf 🍁 (1 units)
  - Total gross: 2840.00€
  - Total tax: 304.08€
  💸 Net received: 2535.92€

Gold Bar 100g 🪙 (1 units)
  - Total gross: 9036.50€
  - Total tax: 375.21€
  💸 Net received: 8661.29€

💰 Net Gold Value: 11197.21€
==================================================
       🧭  Welcome to Your Assets Dashboard        
==================================================
            What would you like to do?            
==================================================
1. 🪙 Gold Portfolio
2. 📄 Receivables
3. 🏦 Cash Overview
4. 📉 Stock Portfolio
5. 📊 Total Summary
6. 📈 Portfolio Evolution
7. 📤 Send Financial Summary
q. 🚪 Exit
==================================================
👉 Your choice: 2
==================================================
                  📄 Receivables                   
==================================================
📄 Rengar owes you 1000.00€
📄 Katarina owes you 500.00€

💰 Total Receivables: 1500.00€
==================================================
       🧭  Welcome to Your Assets Dashboard        
==================================================
            What would you like to do?            
==================================================
1. 🪙 Gold Portfolio
2. 📄 Receivables
3. 🏦 Cash Overview
4. 📉 Stock Portfolio
5. 📊 Total Summary
6. 📈 Portfolio Evolution
7. 📤 Send Financial Summary
q. 🚪 Exit
==================================================
👉 Your choice: 3
==================================================
             🏦 Cash Holdings Summary              
==================================================
🏠 Home Cash: 100.00€
🏦 Checking Account: 200.00€
📘 Livret A: 1000.00€
🌱 LDDS: 500.00€
🏛️  BFM: 300.00€

🤑 Total Cash: 2100.00€
==================================================
       🧭  Welcome to Your Assets Dashboard        
==================================================
            What would you like to do?            
==================================================
1. 🪙 Gold Portfolio
2. 📄 Receivables
3. 🏦 Cash Overview
4. 📉 Stock Portfolio
5. 📊 Total Summary
6. 📈 Portfolio Evolution
7. 📤 Send Financial Summary
q. 🚪 Exit
==================================================
👉 Your choice: 4
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
1. 🪙 Gold Portfolio
2. 📄 Receivables
3. 🏦 Cash Overview
4. 📉 Stock Portfolio
5. 📊 Total Summary
6. 📈 Portfolio Evolution
7. 📤 Send Financial Summary
q. 🚪 Exit
==================================================
👉 Your choice: 5
==================================================
           📈 Overall Financial Summary            
==================================================
💰 Gold: 11197.21€
📄 Receivables: 1500.00€
🏦 Cash: 2100.00€
📈 Stocks: 1280.00€

💼 Total Portfolio Value: 16077.21€
==================================================
       🧭  Welcome to Your Assets Dashboard        
==================================================
            What would you like to do?            
==================================================
1. 🪙 Gold Portfolio
2. 📄 Receivables
3. 🏦 Cash Overview
4. 📉 Stock Portfolio
5. 📊 Total Summary
6. 📈 Portfolio Evolution
7. 📤 Send Financial Summary
q. 🚪 Exit
==================================================
👉 Your choice: 6
==================================================
==================================================
         📊 Portfolio Evolution Over Time          
==================================================
Mar 2025 | ███████████████████████████ 11066.12 €
Apr 2025 | ████████████████████████████████████████ 16077.21 €
==================================================
       🧭  Welcome to Your Assets Dashboard        
==================================================
            What would you like to do?            
==================================================
1. 🪙 Gold Portfolio
2. 📄 Receivables
3. 🏦 Cash Overview
4. 📉 Stock Portfolio
5. 📊 Total Summary
6. 📈 Portfolio Evolution
7. 📤 Send Financial Summary
q. 🚪 Exit
==================================================
👉 Your choice: 7
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
1. 🪙 Gold Portfolio
2. 📄 Receivables
3. 🏦 Cash Overview
4. 📉 Stock Portfolio
5. 📊 Total Summary
6. 📈 Portfolio Evolution
7. 📤 Send Financial Summary
q. 🚪 Exit
==================================================
👉 Your choice: q
==================================================
👋 Goodbye! See you soon.
==================================================
```