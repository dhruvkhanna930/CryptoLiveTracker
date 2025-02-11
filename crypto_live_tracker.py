import requests
import pandas as pd
from dotenv import load_dotenv
import os
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from fpdf import FPDF

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
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Name": crypto["name"],
            "Symbol": crypto["symbol"],
            "Price (USD)": crypto["quote"]["USD"]["price"],
            "Market Cap": crypto["quote"]["USD"]["market_cap"],
            "24h Volume": crypto["quote"]["USD"]["volume_24h"],
            "24h Price Change (%)": crypto["quote"]["USD"]["percent_change_24h"]
        }
        crypto_list.append(crypto_dict)
    return pd.DataFrame(crypto_list)


def authenticate_google_sheets():
    SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_file("credentials.json", scopes=SCOPES)
    client = gspread.authorize(creds)
    return client


def upload_to_google_sheets(df, sheet_name):
    client = authenticate_google_sheets()
    try:
        sheet = client.open(sheet_name)  
    except gspread.exceptions.APIError:
        sheet = client.create(sheet_name)  

    worksheet = sheet.get_worksheet(0)  
    worksheet.clear()  
    worksheet.update([df.columns.values.tolist()] + df.values.tolist()) 

    sheet_id = sheet.id
    sheet_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}"

    creds = Credentials.from_service_account_file("credentials.json", scopes=["https://www.googleapis.com/auth/drive"])
    drive_service = build("drive", "v3", credentials=creds)

    try:
        drive_service.permissions().create(
            fileId=sheet_id,
            body={"role": "reader", "type": "anyone"},
        ).execute()
        print(f"Data uploaded successfully! View it here: {sheet_url}")
    except HttpError as error:
        print(f"An error occurred: {error}")

    return sheet_url


# 2-Data Analysis
def analyze_data(df):
    top_5_by_market_cap = df.sort_values(by="Market Cap", ascending=False).head(5)
    top_5_names = ", ".join(top_5_by_market_cap["Name"].tolist())

    average_price = df["Price (USD)"].mean()

    highest_change_row = df.loc[df["24h Price Change (%)"].idxmax()]
    lowest_change_row = df.loc[df["24h Price Change (%)"].idxmin()]

    highest_change = f"{highest_change_row['24h Price Change (%)']:.2f}% ({highest_change_row['Name']})"
    lowest_change = f"{lowest_change_row['24h Price Change (%)']:.2f}% ({lowest_change_row['Name']})"

    df["Top 5 by Market Cap"] = top_5_names
    df["Average Price (Top 50)"] = average_price
    df["Highest 24h Change (%)"] = highest_change
    df["Lowest 24h Change (%)"] = lowest_change

    return df



data = fetch_crypto_data()
df = parse_data(data)
df = analyze_data(df)

df.to_excel("crypto_data.xlsx", index=False)
print("Data saved to crypto_data.xlsx")
upload_to_google_sheets(df, "CryptoLiveTracker")
# print("Data uploaded successfully! View it here: https://docs.google.com/spreadsheets/d/1AbCDEfgHIJKLMNOpQRstuVwXYZ1234567890")