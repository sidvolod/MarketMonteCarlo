import numpy as np

def generate_price_paths (stats: dict, days: int, iterations: int):
    """
        Generates a matrix of simulated future price paths by
        applying principles of Geometric Brownian Motion (GBM).
    Args:
        stats (dict): Dictionary with statistics of the data with keys:
            mu: mean, sigma: standard deviation, and last price.
    Returns:
        np.ndarray: a 2-dimensional matrix of shape (iterations X days+1).
    """

    mu = stats["mu"]
    sigma = stats["sigma"]
    last_price = stats["last price"]

    drift = (mu - 0.5*(sigma**2))
    shock_z_matrix = sigma * np.random.standard_normal((iterations, days))
    daily_change = np.exp(drift + shock_z_matrix)

    price_paths = last_price * np.cumprod(daily_change, axis=1)
    price_paths = np.hstack((np.full((iterations,1),last_price), price_paths))