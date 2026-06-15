import logging

from .models import Ticker
import requests
import json
import pandas as pd
from typing import Any
logger = logging.getLogger(__name__)
logging.basicConfig(filename='./logs.txt', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

class MissingAPIKeyError(Exception):
    """There is no API key available in .env file"""

class DataFetchError(Exception):
    """There is an error fetching data from the API"""

def get_market_data (ticker : Ticker, API_KEY : str) -> dict[str, Any]:
    """
    Fetches market data for given ticker from Finage API

    Args:
        ticker (Ticker): Instance of the Ticker class
        API_KEY (str): API key for finage API
    Returns:
        (Json-Object): JSON data from the API
    """

    if not API_KEY:
        logger.error("No API key provided")
        raise MissingAPIKeyError("No API key provided")

    url = ticker.get_api_url_endpoint()
    params = {"apikey": API_KEY}
    logger.info(f"Fetching market data from Finage API {url}")
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        with open("data/market_data.json", "w", encoding="utf-8") as file:
            file.write(json.dumps(data, indent=4))
        logger.info(f"Successfully fetched data for {ticker.symbol}")

        return data

    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTP error: {e.response.status_code} for {url}")
    except requests.exceptions.RequestException:
        logger.error(f"Connection error: Could not reach Finage for {ticker.symbol}")

    raise DataFetchError(f"Could not fetch data for {ticker.symbol}")

def process_data_to_dataframe(data : dict[str,Any]) -> pd.DataFrame:
    """
    Parses raw JSON from Finage API into a cleaned Pandas DataFrame

    Args:
        data (JSON-Object): JSON object with market data
    Returns:
        pd.DataFrame: cleaned OHLCV data indexed by datetime
    """

    if not "results" in data:
        logger.error("No data found in the response")
        raise DataFetchError("No data found in the response")

    df = pd.DataFrame(data["results"])
    df = df.rename(columns={"o": "Open", "h": "High", "l": "Low",
                            "c": "Close", "v": "Volume"})

    df["Date"] = pd.to_datetime(df["t"], unit="ms")
    df = df.set_index("Date")

    return df[["Open", "High", "Low", "Close", "Volume"]]
