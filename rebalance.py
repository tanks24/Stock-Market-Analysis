import numpy as np
import pandas as pd

def mean_variance_optimizer(data_dict):
    returns = pd.concat([df['Close'].pct_change() for df in data_dict.values()], axis=1)
    returns.columns = list(data_dict.keys())
    cov_matrix = returns.cov()
    mean_returns = returns.mean()

    inv_cov = np.linalg.pinv(cov_matrix)
    weights = inv_cov @ mean_returns
    weights /= weights.sum()
    return weights.round(2)
