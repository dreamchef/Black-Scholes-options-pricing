r2_values_bid = []
r2_values_ask = []
volatility_frequencies = []

for label in volatility_labels:
    subset = options_data[options_data['Volatility_Range'] == label]
    if not subset.empty:
        r2_bid = r2_score(subset['bid'], subset['Predicted Call Price'])
        r2_ask = r2_score(subset['ask'], subset['Predicted Call Price'])
    else:
        r2_bid = np.nan  # Use NaN to indicate no data
        r2_ask = np.nan

    frequency = len(subset)
    r2_values_bid.append(r2_bid)
    r2_values_ask.append(r2_ask)
    volatility_frequencies.append(frequency)

plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
plt.bar(volatility_labels, volatility_frequencies, color='skyblue')
plt.title('Frequency of Different Volatility Ranges')
plt.xlabel('Volatility Range')
plt.ylabel('Frequency')

plt.subplot(1, 2, 2)
bar_width = 0.35
index = np.arange(len(volatility_labels))

bar1 = plt.bar(index, r2_values_bid, bar_width, label='R² vs Bid', color='orange')
bar2 = plt.bar(index + bar_width, r2_values_ask, bar_width, label='R² vs Ask', color='green')

plt.title('R² Values for Different Volatility Ranges')
plt.xlabel('Volatility Range')
plt.ylabel('R² Value')
plt.xticks(index + bar_width / 2, volatility_labels)
plt.legend()

plt.tight_layout()
plt.show()

