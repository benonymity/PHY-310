import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import find_peaks

def plot_data(filename, expected_freq):
    # Load data from file
    data = np.loadtxt(filename, skiprows=8)
    time = data[:, 0]
    potential = data[:, 1]

    # Find peaks with prominence to calculate frequency
    peaks, _ = find_peaks(potential, prominence=0.5)
    if len(peaks) > 1:
        # Calculate frequency from peak-to-peak intervals
        peak_intervals = np.diff(time[peaks])
        actual_freq = 1 / np.mean(peak_intervals)
    else:
        actual_freq = None

    # Generate sine wave with expected frequency
    amplitude = (np.max(potential) - np.min(potential)) / 2
    offset = (np.max(potential) + np.min(potential)) / 2
    
    # Estimate phase shift
    initial_position = potential[0]
    phase_shift = np.arcsin((initial_position - offset) / amplitude)
    if potential[1] < potential[0]:
        phase_shift = np.pi - phase_shift
    
    expected_sine = amplitude * np.sin(2 * np.pi * expected_freq * time + phase_shift) + offset

    # Plot the data
    plt.figure(figsize=(10, 6))
    plt.plot(time, potential, label='Actual Data')
    plt.plot(time, expected_sine, ':', label='Expected Sine Wave')
    plt.title(f'{filename} (Expected: {expected_freq} Hz, Actual: {actual_freq:.2f} Hz)')
    plt.xlabel('Time (s)')
    plt.ylabel('Potential (V)')
    plt.grid(True)
    plt.legend()

files_and_freqs = [('1 Hz.txt', 1), ('10 Hz.txt', 10), ('100 Hz.txt', 100)]

for file, freq in files_and_freqs:
    plot_data(file, freq)
    plt.savefig(f'{file[:-4]}.png')  # Save each plot as a PNG file
    plt.tight_layout()
    plt.show()

