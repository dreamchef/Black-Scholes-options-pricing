import numpy as np
import scipy.stats as si
import pandas as pd
from sklearn.metrics import r2_score

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
    if sigma == 0 or T == 0:  # Handling cases where volatility or time to maturity is zero
        return 0

    d1 = (np.log(S / X) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    call_price = (S * si.norm.cdf(d1, 0.0, 1.0) - X * np.exp(-r * T) * si.norm.cdf(d2, 0.0, 1.0))
    return call_price

# File path for the uploaded CSV
file_path = '/mnt/data/calls_dataset.csv'

# Loading the CSV file
df_calls = pd.read_csv(file_path)

# Setting a constant risk-free rate for all options (4.23% in this case)
risk_free_rate = 0.0423

# Filtering out rows with extremely high volatility
df_filtered = df_calls[df_calls['impliedVolatility'] <= 3]

# Recalculating the call prices for the filtered data
df_filtered['Predicted Call Price'] = df_filtered.apply(
    lambda row: black_scholes_call(
        S=row['price'],
        X=row['strike'],
        T=row['remaining'] / 365,  # converting days to years
        r=risk_free_rate,
        sigma=row['impliedVolatility']
    ),
    axis=1
)

# Further cleaning to remove any NaN or infinite values in the columns 'bid', 'ask', and 'Predicted Call Price'
df_filtered_clean = df_filtered.dropna(subset=['bid', 'ask', 'Predicted Call Price'])
df_filtered_clean = df_filtered_clean.replace([np.inf, -np.inf], np.nan).dropna(subset=['bid', 'ask', 'Predicted Call Price'])

# Saving the cleaned and updated DataFrame to a new CSV file
output_csv_path_new_predictions = '/mnt/data/predicted_call_prices_new.csv'
df_filtered_clean.to_csv(output_csv_path_new_predictions, index=False)
