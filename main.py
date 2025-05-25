from yahooquery import Ticker
import pandas as pd
from datetime import datetime

from ind import calculate_sma, calculate_rsi
from visualize import plot_stock, plot_forecast
from forecast import forecast_prices

def fetch_data(ticker, start='2022-01-01', end='2023-01-01'):
    try:
        stock = Ticker(ticker)
        df = stock.history(start=start, end=end)
        
        if df.empty:
            print(f"No data found for ticker '{ticker}'.")
            return None
        if isinstance(df.index, pd.MultiIndex):
            df = df.xs(ticker, level=0)

        df = df.reset_index()
        df = df.rename(columns={col: col.capitalize() for col in df.columns})

        return df
    except Exception as e:
        print(f"Failed to fetch data for '{ticker}': {e}")
        return None

def clean_date(prompt_text, default=None):
    while True:
        user_input = input(prompt_text).strip()
        if not user_input and default:
            return default
        try:
            # Accepts YYYY-MM-DD or YYYY/MM/DD
            date_obj = datetime.strptime(user_input, "%Y-%m-%d")
            return date_obj.strftime("%Y-%m-%d")
        except ValueError:
            try:
                date_obj = datetime.strptime(user_input, "%Y/%m/%d")
                return date_obj.strftime("%Y-%m-%d")
            except ValueError:
                print("Invalid date format. Please use YYYY-MM-DD.")

if __name__ == "__main__":
    ticker = input("Enter the stock ticker symbol: ").upper().strip()
    today = datetime.today().strftime("%Y-%m-%d")
    start = clean_date("Enter the start date (YYYY-MM-DD): ", default="2022-01-01")
    end = clean_date(f"Enter the end date (YYYY-MM-DD) [default: {today}]: ", default=today)

    df = fetch_data(ticker, start, end)

    if df is not None:
        print(df.describe())
        df = calculate_sma(df)
        df = calculate_rsi(df)
        plot_stock(df, ticker)

        #ARIMA parameters
        try:
            p = int(input("ARIMA p (default 5): ") or 5)
            d = int(input("ARIMA d (default 1): ") or 1)
            q = int(input("ARIMA q (default 0): ") or 0)
        except ValueError:
            p, d, q = 5, 1, 0

        steps = int(input("Forecast steps (days, default 30): ") or 30)
        forecast, conf_int = forecast_prices(df, steps=steps, arima_order=(p, d, q))
        print("\nForecasted Close Prices for next {} days:".format(steps))
        print(forecast)

        plot_forecast(df, forecast, conf_int, ticker)
    else:
        print("No data to plot.")

