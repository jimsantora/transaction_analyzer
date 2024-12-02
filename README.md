# Transaction Analyzer 📊

Analyze your bank transactions and get beautiful visualizations of your spending patterns. Groups similar merchants together, categorizes spending, and shows your financial flows.

## Features 🚀

- Merchant name normalization (e.g., "WAL-MART", "WALMART.COM" → "WALMART")
- Spending category detection
- Interactive spending flow diagram
- Monthly/yearly averages
- Beautiful HTML reports
- Smart handling of transfers and Zelle payments

## Quick Start 🏃‍♂️

```bash
# Basic usage - outputs text report
python script.py transactions.csv

# Generate HTML report
python script.py transactions.csv --format html --output report.html
```

## Input Format 📝

Your CSV should have these columns:
- Date
- Amount (positive for deposits, negative for spending)
- Description (merchant name/transaction description)

Example:
```csv
Date,Amount,Description
2024-01-01,-50.25,WALMART.COM
2024-01-02,-12.99,NETFLIX
2024-01-03,1000.00,PAYCHECK DEPOSIT
```

## Customization 🛠️

Add new merchant categories in `categories.py`:

```python
TRANSACTION_CATEGORIES = {
    'Entertainment': ['NETFLIX', 'HULU', 'SPOTIFY'],
    'Shopping': ['WALMART', 'TARGET', 'AMAZON'],
    # Add your categories...
}
```

## Requirements 📦

```bash
pip install pandas numpy thefuzz tqdm
```

## Output Examples 🎨

Text mode shows:
- Top merchants by spending
- Total money flows
- Monthly/yearly averages

HTML mode adds:
- Interactive category flow diagram 
- Color-coded spending visualization
- Tooltips showing category keywords
- Responsive design for mobile viewing

## License 📄

MIT License. Use it however you want!