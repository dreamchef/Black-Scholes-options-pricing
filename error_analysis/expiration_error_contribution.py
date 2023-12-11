import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score

# Define remaining time ranges.
time_bins = [0, 10, 20, 30, 40, np.inf]  # Example ranges
time_labels = ['0-10', '10-20', '20-30', '30-40', '>40']
options_data['Time_Range'] = pd.cut(options_data['remaining'], bins=time_bins, labels=time_labels, right=False)

r2_values_bid_time = []
r2_values_ask_time = []
time_frequencies = []

for label in time_labels:
    subset = options_data[options_data['Time_Range'] == label]
    if not subset.empty:
        r2_bid_time = r2_score(subset['bid'], subset['Predicted Call Price'])
        r2_ask_time = r2_score(subset['ask'], subset['Predicted Call Price'])
    else:
        r2_bid_time = np.nan  # Use NaN to indicate no data
        r2_ask_time = np.nan

    frequency = len(subset)
    r2_values_bid_time.append(r2_bid_time)
    r2_values_ask_time.append(r2_ask_time)
    time_frequencies.append(frequency)

plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
plt.bar(time_labels, time_frequencies, color='skyblue')
plt.title('Frequency of Different Remaining Time Ranges')
plt.xlabel('Remaining Time Range')
plt.ylabel('Frequency')

plt.subplot(1, 2, 2)
bar_width = 0.35
index = np.arange(len(time_labels))

plt.bar(index, r2_values_bid_time, bar_width, label='R² vs Bid', color='orange')
plt.bar(index + bar_width, r2_values_ask_time, bar_width, label='R² vs Ask', color='green')

plt.title('R² Values for Different Remaining Time Ranges')
plt.xlabel('Remaining Time Range')
plt.ylabel('R² Value')
plt.xticks(index + bar_width / 2, time_labels)
plt.legend()

plt.tight_layout()
plt.show()
