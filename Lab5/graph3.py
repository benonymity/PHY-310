import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

def get_peak_emf(file_path):
    df = pd.read_csv(file_path, skiprows=[0])
    return np.max(np.abs(df.iloc[:, 1]))

def extract_frequency(filename):
    return int(filename.split('Hz')[0])

data_folder = 'data'
csv_files = sorted([f for f in os.listdir(data_folder) if f.endswith('.csv')])

frequencies = []
peak_emfs = []

for file in csv_files:
    file_path = os.path.join(data_folder, file)
    frequency = extract_frequency(file)
    peak_emf = get_peak_emf(file_path)
    
    frequencies.append(frequency)
    peak_emfs.append(peak_emf)

sorted_data = sorted(zip(frequencies, peak_emfs))
frequencies, peak_emfs = zip(*sorted_data)

slope, intercept, r_value, p_value, std_err = stats.linregress(frequencies, peak_emfs)

plt.figure(figsize=(10, 6))
plt.scatter(frequencies, peak_emfs, color='blue', label='Data')

fit_line = slope * np.array(frequencies) + intercept
plt.plot(frequencies, fit_line, color='red', label='Linear Fit')

plt.xlabel('Frequency (Hz)')
plt.ylabel('Peak EMF (mV)')
plt.title('Peak EMF vs Frequency')

equation = f'EMF = {slope:.2f}f + {intercept:.2f}'
r_squared = f'R² = {r_value**2:.4f}'
plt.text(0.5, 0.95, equation + '\n' + r_squared, transform=plt.gca().transAxes, 
         verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

plt.legend()
plt.grid(True)
plt.tight_layout()

plt.savefig('peak_emf_vs_frequency_fit.png')
plt.show()

print(f"Slope: {slope:.4f} mV/Hz")
print(f"Intercept: {intercept:.4f} mV")
print(f"R-squared: {r_value**2:.4f}")
