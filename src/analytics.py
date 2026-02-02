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
    def __init__(self, price_matrix, len_history, annual_periods = 252):
        """
            Constructor for initialization of Analytics object.

            Parameters:
                price_matrix (np.Ndarray): price matrix of our simulations
                start_price (float): start price of simulation
                len_history (int): length of data used for simulations
                let_simulation (int): amount of simulated timeframes
                annual_periods (int): number of datapoints that make up one year
                _drawdown_cache (Ndarray): cache for drawdown matrix
                _log_return_cache (Ndarray): cache for log return matrix
        """
        self.price_matrix = price_matrix
        self.start_price = price_matrix[0, 0]
        self.len_history = len_history
        self.len_simulation = price_matrix.shape[1]-1
        self.annual_periods = annual_periods
        self._drawdown_cache = None
        self._log_return_cache = None

    def get_final_stats (self):
        """
            Analyses the price matrix and returns the final statistics.
            Consists of mean, probability of profit and final spread
            of the price matrix.
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

    def get_annualized_volatility(self):
        """
            Calculates the annualized volatility.

            Returns:
                volatility (float): annualized volatility.
        """
        log_returns = self._calculate_log_return_matrix()
        volatility = np.std(log_returns)
        return volatility * np.sqrt(self.annual_periods)

    def get_risk_metrics (self):
        """
            Calculates the Value at Risk (VaR) of the price
            and Conditional Value at Risk (CVar) showing if the price
            goes below fifth percentile on average how bad is it.
            Utilizes generally accepted threshold of 5th percentile

        Returns:
            (dict): a dicitonary containing 'var' and 'cvar' values.
        """
        final_price = self.price_matrix[:, -1]
        fifth_perc = np.percentile(final_price, 5)

        var_dollar = self.start_price - fifth_perc
        cvar_dollar =  self.start_price - np.mean(final_price[final_price < fifth_perc])

        var_pct = var_dollar / self.start_price
        cvar_pct = cvar_dollar / self.start_price

        return {
            "var_dollar": var_dollar,
            "cvar_dollar": cvar_dollar,
            "var_pct": var_pct,
            "cvar_pct": cvar_pct,
        }

    def _calculate_drawdown_matrix (self):
        """
            A helper function to calculate drawdown matrix.

            Returns:
                drawdown_matrix (np.Ndarray): drawdown matrix
        """
        if self._drawdown_cache is None:
            peaks = np.maximum.accumulate(self.price_matrix, axis=1)
            self._drawdown_cache = (peaks - self.price_matrix)/peaks
        return self._drawdown_cache

    def _calculate_log_return_matrix (self):
        if self._log_return_cache is None:
            self._log_return_cache = np.diff(np.log(self.price_matrix), axis=1)
        return self._log_return_cache

    def get_average_maximum_drawdown (self):
        """
            Calculates average maximum drawdown of the price matrix.
            Returns:
                 average_drawdown (float): average maximum drawdown of the price matrix
        """
        drawdown = self._calculate_drawdown_matrix()
        maximum_drawdown = np.max(drawdown, axis=1)
        average_worst_drawdown = np.percentile(maximum_drawdown, 95)
        return average_worst_drawdown

    def get_ulcer_index (self):
        """
            Calculates Ulcer index of the price matrix.
            A metric representing how long and deep are the drawdowns

            Returns:
                ulcer_index (int): ulcer index of the price matrix
        """
        drawdown = self._calculate_drawdown_matrix()
        squared_mean_drawdown = np.mean(np.square(drawdown), axis=1)
        return np.mean(np.sqrt(squared_mean_drawdown))

    def get_expected_sharpe_ratio(self, risk_free_rate):
        """
            Calculates the expected Sharpe Ratio of the simulations

            Returns:
                expected_sharpe_ratio (float): expected Sharpe Ratio
                                               of the simulations
        """
        period_return = self._calculate_log_return_matrix()
        rf_rate_period = np.log(1 + risk_free_rate) / self.annual_periods
        std_dev = np.std(period_return)
        mean = np.mean(period_return)
        sharpe_ratio = (mean - rf_rate_period) / std_dev

        return sharpe_ratio * np.sqrt(self.annual_periods)

    def get_expected_sortino_ratio(self, risk_free_rate):
        """
            Calculates the expected Sortino Ratio of the simulations

            Returns:
                expected_sortino_ratio (float): expected Sortino Ratio
        """
        rf_rate_period = np.log(1 + risk_free_rate) / self.annual_periods
        period_return = self._calculate_log_return_matrix()

        excess_return = period_return - rf_rate_period
        downside_returns = np.where(excess_return < 0, excess_return, 0)
        root_mean_square_return = np.sqrt(np.mean(np.square(downside_returns)))
        mean = np.mean(period_return)
        if root_mean_square_return == 0:
            return 0
        sortino_ratio = (mean - rf_rate_period) / root_mean_square_return

        return sortino_ratio * np.sqrt(self.annual_periods)

    def validity_check (self):
        """
            Checks if the length of history is enough to simulate the future

            Returns:
                 result (dict): Dictionary with status and reason for it
        """
        result = {"status": "", "reason" : ""}
        if self.len_simulation > 0.5 * self.len_history:
            result["status"] = "Critical"
            result["reason"] = "Not enough historical data for simulation of this length"
            return result
        elif self.len_simulation > 0.3 * self.len_history:
            result["status"] = "Warning"
            result["reason"] = "Simulation duration is long relative to historical data"
            return result
        else:
            result["status"] = "Safe"
            result["reason"] = ""
            return result

    def get_summary (self, risk_free_rate = 0.04):
        """
            Returns summary statistics of the Monte-Carlo simulation.

            Returns:
                (dict): Containing Metadata, performance and risk metrics
                for the simulation.
        """
        final_stats = self.get_final_stats()
        risk = self.get_risk_metrics()
        validity = self.validity_check()
        volatility = self.get_annualized_volatility()
        return {
            "metadata" : {
                "start_price": float(self.start_price),
                "history_length": self.len_history,
                "simulation_length": self.len_simulation,
                "validity_check": validity
            },
            "performance": {
                "mean_final_price": float(final_stats["mean"]),
                "volatility": float(volatility),
                "final_spread": float(final_stats["std_dev"]),
                "probability_of_profit": float(final_stats["probability_of_profit"])
            },
            "risk": {
                "ulcer_index": float(self.get_ulcer_index()),
                "average_maximum_drawdown": float(self.get_average_maximum_drawdown()),
                "value_at_risk_dollar": float(risk["var_dollar"]),
                "value_at_risk_pct": float(risk["var_pct"]),
                "conditional_var_dollar": float(risk["cvar_dollar"]),
                "conditional_var_pct": float(risk["cvar_pct"]),
                "sortino_ratio": float(self.get_expected_sortino_ratio(risk_free_rate)),
                "sharpe_ratio": float(self.get_expected_sharpe_ratio(risk_free_rate))
            }
        }