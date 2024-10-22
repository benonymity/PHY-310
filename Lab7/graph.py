import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.fft import fft, fftfreq

df = pd.read_csv('data/all.csv')

time = df['Latest: Time (s)'].values
potential = df['Latest: Potential (V)'].values

time_step = time[1] - time[0]

def process_chunk(chunk_time, chunk_potential):
    n = len(chunk_time)
    fft_result = fft(chunk_potential)
    frequencies = fftfreq(n, time_step)
    magnitude_spectrum = np.abs(fft_result)
    
    peak_index = np.argmax(magnitude_spectrum[1:]) + 1
    peak_frequency = frequencies[peak_index]
    peak_voltage = magnitude_spectrum[peak_index] / n * 2
    
    return peak_frequency, peak_voltage

chunk_size = 10000
peak_frequencies = []
peak_voltages = []

prev_frequency = None
frequency_change_threshold = 0.1

for i in range(0, len(time) - chunk_size, chunk_size):
    chunk_time = time[i:i+chunk_size]
    chunk_potential = potential[i:i+chunk_size]
    freq, volt = process_chunk(chunk_time, chunk_potential)
    
    if prev_frequency is not None:
        frequency_diff = abs(freq - prev_frequency)
        
        if frequency_diff > frequency_change_threshold:
            print(f"Frequency change detected: {prev_frequency:.2f} Hz -> {freq:.2f} Hz")
    
    prev_frequency = freq
    peak_frequencies.append(freq)
    peak_voltages.append(volt)

freq_voltage_dict = {}

for freq, voltage in zip(peak_frequencies, peak_voltages):
    if freq not in freq_voltage_dict:
        freq_voltage_dict[freq] = voltage
    else:
        freq_voltage_dict[freq] = max(freq_voltage_dict[freq], voltage)

highest_frequencies = list(freq_voltage_dict.keys())
highest_voltages = list(freq_voltage_dict.values())

plt.figure(figsize=(12, 6))
plt.scatter(highest_frequencies, highest_voltages, alpha=0.6)

plt.title('Average Peak Voltage vs Frequency')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Average Peak-to-Peak Voltage (V)')
plt.grid(True)

plt.show()
plt.savefig('images/avg_peak_voltage_vs_frequency.png')
plt.close()

for freq, voltage in zip(avg_frequencies, avg_voltages):
    print(f"Frequency: {freq:.2f} Hz, Average Peak-to-Peak Voltage: {voltage:.2f} V")
