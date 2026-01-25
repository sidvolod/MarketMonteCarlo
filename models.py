class Ticker:
    def __init__(self, symbol, asset_type, multiplier=1, timespan="day"):
        self.symbol = symbol.upper()
        self.asset_type = asset_type.lower()
        self.multiplier = multiplier
        self.timespan = timespan

        self.from_date = "2024-01-01"
        self.to_date = "2024-01-31"

    def get_api_url_endpoint(self):
        base_url = f"https://api.finage.co.uk/agg/{self.asset_type}"

        return f"{base_url}/{self.symbol}/{self.multiplier}/{self.timespan}/{self.from_date}/{self.to_date}"

    def __str__(self):
        return f"Ticker Object: {self.symbol} ({self.asset_type})"

