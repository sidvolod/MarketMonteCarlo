import pandas as pd
import numpy as np

def calculate_analytics(data : pd.DataFrame):
    log_returns = np.log(data["Close"]/data["Close"].shift(1)).dropna()
    return {
        "mu": log_returns.mean(),
        "sigma": log_returns.std() ,
        "last price": data["Close"].iloc[-1],
    }
class Analytics:
    def __init__(self, price_matrix, len_history):
        self.price_matrix = price_matrix
        self.start_price = price_matrix[0, 0]
        self.len_history = len_history
        self.len_simulation = price_matrix.shape[1]-1
        self._drawdown_cache = None

    def get_final_stats (self):
        """
            Analyses the price matrix and returns the final statistics.

        Args:
            price_matrix (np.ndarray): matrix of prices from Monte Carlo simulations.
            start_price (float): starting price.

        Returns:
            (dict): dictionary with final statistics.
        """

        final_price = self.price_matrix[:, -1]
        mean = np.mean(final_price)
        std_dev = np.std(final_price)

        # When we applied .greater it returned a True/False matrix
        # when we applied .mean to resulting matrix we converted Boolean values
        # to 1s and 0s and mean calculated sum of 1s (success)/ all cases
        # giving us the probability of success
        probability_of_profit = np.mean(np.greater(final_price, self.start_price))

        return {
            "mean": mean,
            "probability_of_profit": probability_of_profit,
            "std_dev": std_dev,
        }

    def calculate_var (self):
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
        final_price = self.price_matrix[:, -1]
        fifth_perc = np.percentile(final_price, 5)

        worst_case = np.mean(final_price[final_price < fifth_perc])


        return {
            "var": self.start_price - fifth_perc,
            "cvar": self.start_price - worst_case,
        }

    def _calculate_drawdown_matrix (self):
        if self._drawdown_cache is None:
            peaks = np.maximum.accumulate(self.price_matrix, axis=1)
            self._drawdown_cache = (peaks - self.price_matrix)/peaks
        return self._drawdown_cache

    def get_average_maximum_drawdown (self):
        drawdown = self._calculate_drawdown_matrix()
        maximum_drawdown = np.max(drawdown, axis=1)
        average_worst_drawdown = np.percentile(maximum_drawdown, 95)
        return average_worst_drawdown

    def get_ulcer_index (self):
        drawdown = self._calculate_drawdown_matrix()
        squared_mean_drawdown = np.mean(np.square(drawdown), axis=1)
        return np.mean(np.sqrt(squared_mean_drawdown))

    def validity_check (self):

        if self.len_simulation > 0.5 * self.len_history:
            return "Critical: Not enough historical data for simulation of this length"
        elif self.len_simulation > 0.3 * self.len_history:
            return "Warning: Simulation duration is long relative to historical data"
        else:
            return "Safe"