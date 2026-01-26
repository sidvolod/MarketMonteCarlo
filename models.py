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
    def __init__(self, symbol, asset_type, from_date,
                 to_date, multiplier=1,timespan="day"):

        self.symbol = symbol.upper()
        self.asset_type = asset_type.lower()
        self.multiplier = multiplier
        self.timespan = timespan

        self.from_date = from_date
        self.to_date = to_date

    def get_api_url_endpoint(self):
        """
        Generates the base URL for the Finage aggregate endpoint.

        Returns:
            str: The formatted URL string without the API key suffix.
        """
        base_url = f"https://api.finage.co.uk/agg/{self.asset_type}"

        return (f"{base_url}/{self.symbol}/{self.multiplier}/"
                f"{self.timespan}/{self.from_date}/{self.to_date}")

    def __str__(self):
        return f"Ticker Object: {self.symbol} ({self.asset_type})"

