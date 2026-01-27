import pandas as pd
import numpy as np

def calculate_analytics(data : pd.DataFrame):
    log_returns = np.log(data["Close"]/data["Close"].shift(1)).dropna()
    return {
        "mu": log_returns.mean(),
        "sigma": log_returns.std() ,
        "last price": data["Close"].iloc[-1],
    }
