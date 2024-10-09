import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def extract_frequency(data):
    time = data.iloc[:, 0] 
    voltage = data.iloc[:, 1]
    
    # Remove NaN values
    valid_data = pd.concat([time, voltage], axis=1).dropna()
    time = valid_data.iloc[:, 0]
    voltage = valid_data.iloc[:, 1]
    
    if len(voltage) < 2:
        return None
    
    # Compute the FFT
    fft = np.fft.fft(voltage.astype(float))
    freqs = np.fft.fftfreq(len(time), time.iloc[1] - time.iloc[0])
    
    # Find the peak frequency
    fft_magnitude = np.abs(fft[1:])
    if len(fft_magnitude) > 0:
        peak_freq = freqs[np.argmax(fft_magnitude) + 1]
        return abs(peak_freq)
    else:
        return None

def get_max_voltage(data):
    voltage = data.iloc[:, 1]
    return voltage.max()

data_folder = 'data'
csv_files = sorted([f for f in os.listdir(data_folder) if f.endswith('.csv')])

plt.figure(figsize=(12, 8))

for file in csv_files:
    file_path = os.path.join(data_folder, file)
    df = pd.read_csv(file_path, header=None, skiprows=[0])  # skip first row
    
    # Split the data into chunks of about 1000 rows each
    chunk_size = 1000
    chunks = [df[i:i+chunk_size] for i in range(0, len(df), chunk_size)]
    
    frequencies = []
    max_voltages = []
    
    for chunk in chunks:
        freq = extract_frequency(chunk)
        if freq is not None:
            max_volt = get_max_voltage(chunk)
            frequencies.append(freq)
            max_voltages.append(max_volt)
    
    if frequencies and max_voltages:
        # Sort by frequency
        sorted_data = sorted(zip(frequencies, max_voltages))
        frequencies, max_voltages = zip(*sorted_data)
        
        plt.plot(frequencies, max_voltages, 'o-', label=f'Amplification: {file[:-4]}')


plt.xlabel('Frequency (Hz)')
plt.ylabel('Peak EMF (mV)')
plt.title('Peak EMF vs Frequency for Various Amplifications')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig('peak_emf_vs_frequency.png')
plt.show()
