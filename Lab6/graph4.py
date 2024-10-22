import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from sklearn.metrics import r2_score

# Read the CSV file
df = pd.read_csv('data/10Hz-Square-0.05s.csv')

# Dictionary to rename columns
column_rename = {
    'Latest: Time (s)': 'Time',
    'Latest: Potential 1 (V)': 'Inductor Voltage'
}

# Rename the columns
df = df.rename(columns=column_rename)

# Calculate the natural logarithm of voltage over 3.7
df['Log Voltage'] = np.log(df['Inductor Voltage'] / 3.7)

# Define the linear function for curve fitting
def linear_func(x, m, b):
    return m * x + b

# Select data points 9, 10, and 11
fit_data = df.iloc[8:11]

# Perform curve fitting
popt, _ = curve_fit(linear_func, fit_data['Time'], fit_data['Log Voltage'])

# Calculate R-squared
y_pred = linear_func(fit_data['Time'], *popt)
r_squared = r2_score(fit_data['Log Voltage'], y_pred)

# Create the plot
plt.figure(figsize=(12, 8))
plt.plot(df['Time'], df['Log Voltage'], label='ln(Inductor Voltage / 3.7)')

# Plot the fitted curve
x_fit = np.linspace(fit_data['Time'].min(), fit_data['Time'].max(), 100)
y_fit = linear_func(x_fit, *popt)
plt.plot(x_fit, y_fit, 'r--', label=f'Fitted Line: y = {popt[0]:.2f}x + {popt[1]:.2f}, $R^2$: {r_squared:.4f}')

plt.xlabel('Time (s)')
plt.ylabel('ln(Voltage / 3.7)')
plt.title('Natural Logarithm of Inductor Voltage / 3.7 over Time')
plt.legend()
plt.grid(True)

# Save the plot as a PNG file
plt.savefig('images/inductor-voltage-log.png')
plt.close()
