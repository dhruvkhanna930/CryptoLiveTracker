import requests
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("COINMARKETCAP_API_KEY")


# Step 1- Fetch Live Data
def fetch_crypto_data():
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
    parameters = {
        "start": "1",
        "limit": "50",  
        "convert": "USD" 
    }
    headers = {
        "Accepts": "application/json",
        "X-CMC_PRO_API_KEY": API_KEY
    }

    response = requests.get(url, headers=headers, params=parameters)
    data = response.json()
    return data["data"]

def parse_data(data):
    crypto_list = []
    for crypto in data:
        crypto_dict = {
            "Name": crypto["name"],
            "Symbol": crypto["symbol"],
            "Price (USD)": crypto["quote"]["USD"]["price"],
            "Market Cap": crypto["quote"]["USD"]["market_cap"],
            "24h Volume": crypto["quote"]["USD"]["volume_24h"],
            "24h Price Change (%)": crypto["quote"]["USD"]["percent_change_24h"]
        }
        crypto_list.append(crypto_dict)
    return pd.DataFrame(crypto_list)

data = fetch_crypto_data()
df = parse_data(data)
print(df)



# 2-Data Analysis

top_5_by_market_cap = df.sort_values(by="Market Cap", ascending=False).head(5)
average_price = df["Price (USD)"].mean()
highest_price_change = df["24h Price Change (%)"].max()
lowest_price_change = df["24h Price Change (%)"].min()


print("Top 5 Cryptocurrencies by Market Cap:\n", top_5_by_market_cap)
print("\nAverage Price of Top 50 Cryptocurrencies:", average_price)
print("\nHighest 24h Price Change (%):", highest_price_change)
print("Lowest 24h Price Change (%):", lowest_price_change)
