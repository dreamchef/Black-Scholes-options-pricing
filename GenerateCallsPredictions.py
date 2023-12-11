import numpy as np
import scipy.stats as si
import pandas as pd

def black_scholes_call(S, X, T, r, sigma):
    """
    Calculate the Black-Scholes call option price.

    Parameters:
    S (float): Current stock price
    X (float): Strike price
    T (float): Time to maturity (in years)
    r (float): Risk-free interest rate
    sigma (float): Volatility of the stock's returns
    """
    if sigma == 0 or T == 0:
        return 0

    d1 = (np.log(S / X) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    call_price = (S * si.norm.cdf(d1, 0.0, 1.0) - X * np.exp(-r * T) * si.norm.cdf(d2, 0.0, 1.0))
    return call_price

# Get data from scraped file.
file_path = '/mnt/data/calls_dataset.csv'
df_calls = pd.read_csv(file_path)

# Set risk free rate.
risk_free_rate = 0.423  # Example: 1%

# Generate call prices.
df_calls['Predicted Call Price'] = df_calls.apply(
    lambda row: black_scholes_call(
        S=row['price'],
        X=row['strike'],
        T=row['remaining'] / 365,  # converting days to years
        r=risk_free_rate,
        sigma=row['impliedVolatility']
    ),
    axis=1
)

# Prepare dataframe.
final_df = df_calls[['contractSymbol', 'bid', 'ask', 'Predicted Call Price']]

# Save dataframe to CSV file.
output_csv_path = '/mnt/data/predicted_call_prices.csv'
final_df.to_csv(output_csv_path, index=False)
