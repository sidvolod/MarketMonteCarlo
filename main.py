import os
import requests
import models
import json
import pandas as pd
from dotenv import load_dotenv

def get_market_data (ticker):


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
if __name__ == "__main__":
    dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
    load_dotenv(dotenv_path)

    ticker = models.Ticker(asset_type="crypto", symbol="BTCUSD")

    # data = get_market_data(ticker)
    with open("data/market_data.json", "r", encoding="utf-8") as file:
        data = json.load(file)
    # data_frame = pd.DataFrame(data["results"])
    # data_frame = data_frame.rename(columns={"o": "open", "h": "high", "l": "low", "c": "close", "v": "volume", "t": "time"})
    # data_frame["time"] = pd.to_datetime(data_frame["time"], unit="ms")
    # data_frame.set_index("time", inplace=True)
    # print(data_frame.to_string(index=True))
