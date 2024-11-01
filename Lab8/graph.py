import pandas as pd
import matplotlib.pyplot as plt
import os

df = pd.read_csv('data/voltage.csv')

potential = df['Latest: Potential (mV)']
position = df['Latest: Position (m)']

# Calculate rolling average with a window of 10 points
rolling_potential = potential.rolling(window=10, center=True).mean()

plt.figure(figsize=(10, 6))
# Plot both raw and smoothed data
plt.plot(position, potential, 'lightgray', alpha=0.9, label='Raw Data')
plt.plot(position, rolling_potential, 'blue', label='Rolling Average')
plt.title('Potential vs Distance')
plt.xlabel('Distance (m)')
plt.ylabel('Potential (mV)')
plt.grid(True)
plt.legend()
os.makedirs('images', exist_ok=True)
plt.savefig('images/potential_vs_distance.png')
plt.close()

print(f"Plot saved as 'images/potential_vs_distance.png'")
