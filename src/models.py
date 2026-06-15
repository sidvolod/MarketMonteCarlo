from dataclasses import dataclass
@dataclass
class Ticker:

    """
    Financial ticker and its configuration for the Finage API.

    Attributes:
        symbol (str): Ticker symbol (e.g. BTCUSD, AAPL).
        asset_type (str): Asset category (e.g. crypto, stock).
        multiplier (int): Number timespans aggregated (default: 1).
        timespan (str): Time window size (e.g. 'day', 'minute').
        from_date (str): Start date for data collection (format YYYY-MM-DD).
        to_date (str): End date of data collection (format YYYY-MM-DD).

    """
    symbol: str
    asset_type: str
    from_date: str
    to_date: str
    multiplier: int = 1
    timespan: str = "day"


    def get_api_url_endpoint(self):
        """
        Generates the base URL for the Finage aggregate endpoint.

        Returns:
            str: The formatted URL string without the API key suffix.
        """
        base_url = f"https://api.finage.co.uk/agg/{self.asset_type}"

        return (f"{base_url}/{self.symbol}/{self.multiplier}/"
                f"{self.timespan}/{self.from_date}/{self.to_date}")
