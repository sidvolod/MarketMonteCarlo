import numpy as np

class MonteCarloSimulator:
    def __init__(self, stats: dict, days: int, iterations: int, seed: int):
        self.stats = stats
        self.days = days
        self.iterations = iterations
        self.seed: int = None
    def generate_price_paths (self) -> np.ndarray:
        """
            Generates a matrix of simulated future price paths by
            applying principles of Geometric Brownian Motion (GBM).

        Returns:
            np.ndarray: a 2-dimensional matrix of shape (iterations X days+1).
        """
        if self.seed is not None:
            np.random.seed(self.seed)
        mu = self.stats["mu"]
        sigma = self.stats["sigma"]
        last_price = self.stats["last price"]

        drift = (mu - 0.5*(sigma**2))
        shock_z_matrix = sigma * np.random.standard_normal((self.iterations, self.days))
        daily_change = np.exp(drift + shock_z_matrix)

        price_paths = last_price * np.cumprod(daily_change, axis=1)
        price_paths = np.hstack((np.full((self.iterations,1),last_price), price_paths))
        return price_paths

