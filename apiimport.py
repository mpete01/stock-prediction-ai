import requests
import time
import csv
from dotenv import load_dotenv
import os

load_dotenv()

API_key = os.getenv('API_KEY')
ticker = "GOOG"


def get_stock_price(ticker_symbol, api):
    URL = f"https://api.twelvedata.com/time_series?apikey={api}&interval=1day&start_date=2019-03-16 08:00:00&format=JSON&symbol={ticker_symbol}&end_date=2023-11-04 00:00:00&type=stock&dp=2"
    response = requests.get(URL).json()
    csv_filename = f"{ticker_symbol}_data.csv"

    # Open the CSV file in write mode and create a CSV writer
    with open("GOOG.csv", 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        for k, v in response.items():
            if k == "values":
                #print(v)
        # Write the header row (assuming the JSON response is a list of dictionaries)
                if v:
                    header = v[0].keys()
                    csv_writer.writerow(header)
                     # Write the data rows
                    for row in reversed(v):
                        csv_writer.writerow(row.values())
        

stock_price = get_stock_price(ticker, API_key)

print(stock_price)
