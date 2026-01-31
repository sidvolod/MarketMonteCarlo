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
    return price_paths

def get_final_stats (price_matrix, start_price):
    """
        Analyses the price matrix and returns the final statistics.

    Args:
        price_matrix (np.ndarray): matrix of prices from Monte Carlo simulations.
        start_price (float): starting price.

    Returns:
        (dict): dictionary with final statistics.
    """

    final_price = price_matrix[:, -1]
    mean = np.mean(final_price)
    std_dev = np.std(final_price)

    # When we applied .greater it returned a True/False matrix
    # when we applied .mean to resulting matrix we converted Boolean values
    # to 1s and 0s and mean calculated sum of 1s (success)/ all cases
    # giving us the probability of success
    probability_of_profit = np.mean(np.greater(final_price, start_price))

    return {
        "mean": mean,
        "probability_of_profit": probability_of_profit,
        "std_dev": std_dev,
    }

def calculate_var (price_matrix, start_price):
    """
        Calculates the Value at Risk (VaR) of the price
        and Conditional Value at Risk (CVar) showing if the price
        goes below fifth percentile on average how bad is it.
        Utilizes generally accepted threshold of 5th percentile

    Args:
        price_matrix (np.ndarray): matrix of prices from Monte Carlo simulations.
        start_price (float): starting price.
    Returns:
        (dict): a dicitonary containing 'var' and 'cvar' values.
    """
    final_price = price_matrix[:, -1]
    fifth_perc = np.percentile(final_price, 5)

    worst_case = np.mean(final_price[final_price < fifth_perc])


    return {
        "var": start_price - fifth_perc,
        "cvar": start_price - worst_case,
    }
def get_average_maximum_drawdown (price_matrix):

    drawdowns = np.maximum.accumulate(price_matrix, axis=1) - price_matrix
    maximum_drawdown = np.max(drawdowns, axis=1)
    average_worst_drawdown = np.percentile(maximum_drawdown, 95)
    return average_worst_drawdown

def validity_check (len_history, len_simulation):

    if len_simulation > 0.5 * len_history:
        return "Critical: Not enough historical data for simulation of this length"
    elif len_simulation > 0.3 * len_history:
        return "Warning: Simulation duration is long relative to historical data"
    else:
        return "Safe"