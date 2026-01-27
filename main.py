import os
from src import models
from src.analytics import calculate_analytics
from src.scraper import get_market_data, process_data_to_dataframe
import json
from dotenv import load_dotenv


if __name__ == "__main__":
    dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
    load_dotenv(dotenv_path)
    api_key = os.getenv("FINAGE_API_KEY")
    ticker = models.Ticker(asset_type="stock", symbol="AAPL", from_date="2025-12-01", to_date="2025-12-31")


    # with open("data/market_data.json", "r", encoding="utf-8") as file:
    #     data = json.load(file)
    data = get_market_data(ticker, api_key)
    proccessed_data = process_data_to_dataframe(data)
    print(proccessed_data)
    calculate_analytics(proccessed_data)