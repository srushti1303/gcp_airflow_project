import yfinance as yf
import pandas as pd

# Define the stock symbol (Example: Apple)
stock_symbol = "AAPL"

# Fetch historical stock data (last 30 days)
df_stock = yf.download(stock_symbol, period="1mo", interval="1d")

# Save to CSV
df_stock.to_csv(f"{stock_symbol}_stock_data.csv")
print(f"Stock Data Saved: {stock_symbol}_stock_data.csv")
