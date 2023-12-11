import pandas as pd
import numpy as np
import scipy.stats as si

def black_scholes_call(S, X, T, r, sigma):
    if sigma == 0 or T == 0:
        return 0
    d1 = (np.log(S / X) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    call_price = (S * si.norm.cdf(d1, 0.0, 1.0) - X * np.exp(-r * T) * si.norm.cdf(d2, 0.0, 1.0))
    return call_price

def calculate_correlations(csv_file_path):
    df = pd.read_csv(csv_file_path)
    risk_free_rate = 0.0423

    # Fetch predicted call prices.
    df['Predicted Call Price'] = df.apply(
        lambda row: black_scholes_call(row['price'], row['strike'], row['remaining'] / 365, risk_free_rate, row['impliedVolatility']),
        axis=1
    )

    # Calculate correlations.
    correlation_maturity_predicted_price = df['remaining'].corr(df['Predicted Call Price'])
    correlation_volatility_predicted_price = df['impliedVolatility'].corr(df['Predicted Call Price'])

    return correlation_maturity_predicted_price, correlation_volatility_predicted_price

csv_file_path = 'predicted_call_prices.csv'
correlations = calculate_correlations(csv_file_path)
print("Correlation between Time to Maturity and Predicted Call Price:", correlations[0])
print("Correlation between Implied Volatility and Predicted Call Price:", correlations[1])
