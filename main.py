import os
from src import models
from src.analytics import *
from src.scraper import *
from src.simulator import *
from src.visualizer import *
import json
import argparse
from dotenv import load_dotenv

def annual_period_calculator(timespan: str, multiplier: int, asset: str) -> int:
    if asset == "crypto":
        base = {"minute": 525600, "hour": 8760, "day": 365, "week": 52, "month": 12}
    elif asset == "stock":
        base = {"minute": 98280, "hour": 1638, "day": 252, "week": 52, "month": 12}

    base_periods = base.get(timespan.lower(),252)

    return max(1, base_periods//multiplier)

def main():

    parser = argparse.ArgumentParser(description="Monte Carlo Financial Risk Engine")

    # Required parameters
    parser.add_argument("--symbol", required=True, type=str, help="Ticker symbol (e.g. AAPL, BTCUSD).")
    parser.add_argument("--asset", required=True, choices=["stock", "crypto"], type=str, help="Asset category (e.g. crypto, stock).")
    parser.add_argument("--start_date", required=True, type=str, help="Start date (YYYY-MM-DD).)")
    parser.add_argument("--end_date", required=True, type=str, help="End date (YYYY-MM-DD).")
    # Optional arguments with Defaults

    parser.add_argument("--iterations", default=1000, type=int, help="Number of Monte Carlo paths (default: 1000).")
    parser.add_argument("--days", default=252, type=int, help="Number of periods to simulate forward (default: 252).")
    parser.add_argument("--timespan", default="day", type=str, help="Time window size (e.g. 'day', 'minute').")
    parser.add_argument("--multiplier", default=1, type=int, help="Timespans aggregated (default: 1).")
    parser.add_argument("--seed", default=73, type=int, help="Random seed (default: 73).")
    args = parser.parse_args()

    dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
    load_dotenv(dotenv_path)
    api_key = os.getenv("FINAGE_API_KEY")

    ticker = models.Ticker(asset_type=args.asset, symbol=args.symbol, from_date=args.start_date, to_date=args.end_date, multiplier=args.multiplier, timespan=args.timespan)

    data = get_market_data(ticker, api_key)
    proccessed_data = process_data_to_dataframe(data)
    stats = calculate_analytics(proccessed_data)

    simulator = MonteCarloSimulator(stats, args.days, args.iterations, args.seed)
    matrix = simulator.generate_price_paths()

    # History length calculations
    len_history = len(proccessed_data)

    # Annual periods calculator
    annual_periods = annual_period_calculator(args.timespan, args.multiplier, args.asset)

    analytics = Analytics(matrix, len_history, annual_periods)
    viz = Visualizer(analytics)
    viz.plot_simulation()

    plt.tight_layout()
    plt.show()
if __name__ == "__main__":
    main()