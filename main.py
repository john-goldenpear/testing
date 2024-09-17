import yfinance as yf
import cryptocompare
import pandas as pd
from datetime import datetime, timedelta

# Set your API key for CryptoCompare
cryptocompare.cryptocompare._set_api_key_parameter('YOUR_CRYPTO_COMPARE_API_KEY')

# Define the date range
end_date = datetime.now()
start_date = end_date - timedelta(days=1000)  # year of data

# Define the symbols
etf_symbols = {
    'NASDAQ_100': 'QQQ',
    'S&P_500': 'SPY',
    'NASDAQ_CRYPTO_INDEX': 'NCI'
}

crypto_symbols = {
    'ETH/USD': 'ETH',
    'BTC/USD': 'BTC'
}

# Fetch data for ETFs
def fetch_etf_data(symbol, start, end):
    df = yf.download(symbol, start=start, end=end)
    df['Symbol'] = symbol
    return df

# Fetch data for cryptocurrencies
def fetch_crypto_data(symbol, start, end):
    data = cryptocompare.get_historical_price_day(symbol, currency='USD', limit=1000, toTs=end)
    df = pd.DataFrame(data)
    df['time'] = pd.to_datetime(df['time'], unit='s')
    df.set_index('time', inplace=True)
    df['Symbol'] = symbol
    return df

# Fetch ETF data
etf_data = []
for name, symbol in etf_symbols.items():
    data = fetch_etf_data(symbol, start_date, end_date)
    etf_data.append(data)

# Fetch Crypto data
crypto_data = []
for pair, symbol in crypto_symbols.items():
    data = fetch_crypto_data(symbol, start_date, end_date)
    crypto_data.append(data)

# Combine all data
all_data = pd.concat(etf_data + crypto_data)

# Display the data
print(all_data)

# Save to CSV
all_data.to_csv('output/financial_data.csv')

# Optional: Display data in a more readable format if needed
import ace_tools as tools; tools.display_dataframe_to_user(name="Financial Data", dataframe=all_data)
