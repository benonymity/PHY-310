import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file
df = pd.read_csv('data/10Hz-Square-1s.csv')

# Dictionary to rename columns
column_rename = {
    'Latest: Time (s)': 'Time',
    'Latest: Current (A)': 'Current',
    'Latest: Potential 1 (V)': 'Inductor Voltage',
    'Latest: Potential 2 (V)': 'Resistor Voltage'
}

# Rename the columns
df = df.rename(columns=column_rename)

# Create the plot
plt.figure(figsize=(12, 8))
plt.plot(df['Time'], df['Current'], label='Current')
plt.plot(df['Time'], df['Inductor Voltage'], label='Inductor Voltage')
plt.plot(df['Time'], df['Resistor Voltage'], label='Resistor Voltage')

plt.xlabel('Time (s)')
plt.ylabel('Value (mA/V)')
plt.title('10Hz Square Wave')
plt.legend()
plt.grid(True)

# Save the plot as a PNG file
plt.savefig('images/all-square.png')
plt.close()

