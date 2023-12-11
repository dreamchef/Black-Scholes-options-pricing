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
    d1 = (np.log(S / X) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    call_price = (S * si.norm.cdf(d1, 0.0, 1.0) - X * np.exp(-r * T) * si.norm.cdf(d2, 0.0, 1.0))
    return call_price

def calculate_call_prices(input_csv, output_csv):
    """
    Read option data from a CSV file, calculate call prices, and write to another CSV file.

    Parameters:
    input_csv (str): File path for the input CSV file
    output_csv (str): File path for the output CSV file
    """
    # Read the data from CSV
    df = pd.read_csv(input_csv)

    # Calculate call prices
    df['Call Price'] = df.apply(lambda row: black_scholes_call(row['Stock Price'], row['Strike Price'], row['Time to Maturity'], row['Risk-free Rate'], row['Volatility']), axis=1)

    # Write the results to a new CSV file
    df.to_csv(output_csv, index=False)

# Example usage
calculate_call_prices('calls_dataset.csv', 'predicted_call_prices.csv')
