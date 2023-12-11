import pandas as pd

csv_file_path = '/mnt/data/predicted_call_prices_new.csv'
df = pd.read_csv(csv_file_path)

zero_predicted = df[(df['Predicted Call Price'] < 0.01) & ((df['bid'] > 0.01) | (df['ask'] > 0.01))]

high_predicted_low_actual = df[(df['Predicted Call Price'] > 1) & (df['bid'] < 0.01) & (df['ask'] < 0.01)]

summary_zero_predicted = zero_predicted.describe()
summary_high_predicted_low_actual = high_predicted_low_actual.describe()

print(summary_zero_predicted)
print(summary_high_predicted_low_actual)
