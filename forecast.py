from statsmodels.tsa.arima.model import ARIMA
import numpy as np
import pandas as pd
from scipy.optimize import minimize

def optimize_portfolio(prices_df):
    returns = prices_df.pct_change().dropna()
    mean_returns = returns.mean()
    cov_matrix = returns.cov()
    num_assets = len(prices_df.columns)

    def portfolio_variance(weights):
        return np.dot(weights.T, np.dot(cov_matrix, weights))

    def objective(weights):
        return -np.dot(weights, mean_returns) / np.sqrt(portfolio_variance(weights))  # Maximize Sharpe Ratio

    constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    bounds = tuple((0, 1) for _ in range(num_assets))
    init_guess = num_assets * [1. / num_assets]

    result = minimize(objective, init_guess, method='SLSQP', bounds=bounds, constraints=constraints)

    return result.x

def forecast_prices(
    df, 
    steps=30, 
    column='Close', 
    arima_order=(5,1,0), 
    alpha=0.05
):
    close_prices = df[column].dropna()
    model = ARIMA(close_prices, order=arima_order)
    model_fit = model.fit()
    forecast_res = model_fit.get_forecast(steps=steps)
    forecast = forecast_res.predicted_mean
    conf_int = forecast_res.conf_int(alpha=alpha)
    return forecast, conf_int
