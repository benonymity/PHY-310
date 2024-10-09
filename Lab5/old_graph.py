import os
import pandas as pd
import matplotlib.pyplot as plt
import re

def extract_frequency(filename):
    match = re.search(r'(\d+)Hz', filename)
    return int(match.group(1)) if match else None

def get_peak_voltage(df):
    return df['Latest: Potential (mV)'].max()

data_folder = 'data'
frequencies = []
peak_voltages = []

for filename in os.listdir(data_folder):
    if filename.endswith('.csv'):
        frequency = extract_frequency(filename)
        if frequency is not None:
            file_path = os.path.join(data_folder, filename)
            df = pd.read_csv(file_path)
            peak_voltage = get_peak_voltage(df)
            
            frequencies.append(frequency)
            peak_voltages.append(peak_voltage)

# Sort the data by frequency
sorted_data = sorted(zip(frequencies, peak_voltages))
frequencies, peak_voltages = zip(*sorted_data)

plt.figure(figsize=(10, 6))
plt.plot(frequencies, peak_voltages, 'bo-')
# plt.xscale('log')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Peak Voltage (mV)')
plt.title('Peak Voltage vs Frequency')
plt.grid(True)
plt.tight_layout()
plt.savefig('peak_voltage_vs_frequency.png')
plt.show()
