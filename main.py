import os
import requests
import models
import json
import pandas as pd
import numpy as np
from dotenv import load_dotenv

def get_market_data (ticker : models.Ticker):
    """
    Fetches market data for given ticker from Finage API

    Args:
        ticker (Ticker): Instance of the Ticker class
    Returns:
        (Json-Object): JSON data from the API
        None if failed to fetch data
    """

    API_KEY = os.getenv("FINAGE_API_KEY")

    if not API_KEY:
        print("couldnt fetch API key, check .env file")
        return

    url = ticker.get_api_url_endpoint()
    params = {"apikey": API_KEY}
    print(url)
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        with open("data/market_data.json", "w", encoding="utf-8") as file:
            file.write(json.dumps(data, indent=4))
        print(f"Successfully fetched data for {ticker.symbol}")

        return data

    except requests.exceptions.RequestException:
        print(f"Connection error: Could not reach Finage for {ticker.symbol}")
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error: {e.response.status_code} for {url}")
    return None

def process_data_to_dataframe(data):
    """
    Parses raw JSON from Finage API into a cleaned Pandas DataFrame

    Args:
        data (JSON-Object): JSON object with market data
    Returns:
        pd.DataFrame: cleaned OHLCV data indexed by datetime
        None if the results is missing in the JSON
    """

    if not "results" in data:
        print("No data found in the response")
        return None

    df = pd.DataFrame(data["results"])
    df = df.rename(columns={"o": "Open", "h": "High", "l": "Low",
                            "c": "Close", "v": "Volume"})

    df["Date"] = pd.to_datetime(df["t"], unit="ms")
    df.set_index("Date", inplace=True)

    return df[["Open", "High", "Low", "Close", "Volume"]]

if __name__ == "__main__":
    dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
    load_dotenv(dotenv_path)

    ticker = models.Ticker(asset_type="crypto", symbol="BTCUSD")

    # data = get_market_data(ticker)
    with open("data/market_data.json", "r", encoding="utf-8") as file:
        data = json.load(file)