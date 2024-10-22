import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Read the CSV file
df = pd.read_csv('data/10Hz-Square-1s.csv')

# Dictionary to rename columns
column_rename = {
    'Latest: Time (s)': 'Time',
    'Latest: Potential 1 (V)': 'Inductor Voltage'
}

# Rename the columns
df = df.rename(columns=column_rename)

# Take the absolute value of the Inductor Voltage
df['Inductor Voltage'] = np.abs(df['Inductor Voltage'])

# Create the plot
plt.figure(figsize=(12, 8))
plt.plot(df['Time'], df['Inductor Voltage'], label='Inductor Voltage')

plt.xlabel('Time (s)')
plt.ylabel('Absolute Voltage (V)')
plt.title('Absolute Inductor Voltage - 10Hz Square Wave')
plt.legend()
plt.grid(True)

# Save the plot as a PNG file
plt.savefig('images/abs_inductor_voltage_square.png')
plt.close()
