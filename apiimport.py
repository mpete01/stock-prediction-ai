import requests
import csv
from dotenv import load_dotenv
import os
import subprocess
import pycountry
import tkinter as tk
from tkinter import ttk, messagebox

#subprocess.run(["pip", "install", "-r", "requirements.txt"], check=True)
load_dotenv()

API_key = os.getenv('API_KEY')

def get_stock_price(ticker_symbol, country):
    URL = f"https://api.twelvedata.com/time_series?apikey={API_key}&interval=1day&symbol={ticker_symbol}&country={country}&type=stock&format=JSON&outputsize=18&timezone=utc&start_date=2000-10-25 00:00:00&end_date=2024-10-24 00:00:00&dp=2"
    response = requests.get(URL).json()

    if response.get('code') == 404:
        return messagebox.showerror("Error", "Country is not in current subsciption plan to this API. Please try a different one")
    else:
        current_dir = os.getcwd()

        files = [f for f in os.listdir(current_dir) if os.path.isfile(os.path.join(current_dir, f))]

        for file in files:
            name, ext = os.path.splitext(file)
            if ext == ".csv" and name:
                messagebox.showinfo("CSV file already in directory","You already have the stock in a CSV file")
                root.quit()
        # Open the CSV file in write mode and create a CSV writer
        with open(f"{ticker_symbol}.csv", 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            for k, v in response.items():
                if k == "values":
            # Write the header row (assuming the JSON response is a list of dictionaries)
                    if v:
                        header = v[0].keys()
                        csv_writer.writerow(header)
                        # Write the data rows
                        for row in reversed(v):
                            csv_writer.writerow(row.values())
    return response

def get_ticker_symbols(country_code):
    stock_select = tk.Tk()
    URL = f'https://api.twelvedata.com/stocks?country={country_code}'
    response = requests.get(URL).json()["data"]

    #handling if a country has no recorded stocks to be listed
    def country_with_no_stocks():
        stock_select.quit()
        return messagebox.showerror("Error", "Country has no stocks to show within this API")

    if len(response) == 0:
        stock_select.quit()
        return country_with_no_stocks()

    ticker_symbols = [symbol['symbol'] for symbol in response]

    stock_select.title("Select Stock")
    stock_select.geometry("300x150")

    label = tk.Label(stock_select, text="Select or type a stock:")
    label.pack(pady=(10, 0))

    box = ttk.Combobox(stock_select, values=ticker_symbols, width=40)
    box.set(ticker_symbols[0])
    box.pack(pady=10)

    button = tk.Button(stock_select, text="Get Previous Stock Prices", command=lambda: get_stock_price(box.get(), country_code))
    button.pack(pady=10)

    stock_select.mainloop()


def on_select():
    selected_country = combo.get()
    country = pycountry.countries.get(name=selected_country)

    if country:
        messagebox.showinfo("Country Code", f"{selected_country} = {country.alpha_2}")
        get_ticker_symbols(country.alpha_2)
        root.quit()
    else:
        messagebox.showerror("Error", "Country not found!")


countries = sorted([country.name for country in pycountry.countries])
# Create main window
root = tk.Tk()
root.title("Country Picker")
root.geometry("300x150")

#Dropdown menu
label = tk.Label(root, text="Select or type a country:")
label.pack(pady=(10, 0))

combo = ttk.Combobox(root, values=countries, width=40)
combo.set("United States")  # default placeholder
combo.pack(pady=10)

# Button
button = tk.Button(root, text="Get Country Code", command=on_select)
button.pack(pady=10)

# Run the GUI
root.mainloop()