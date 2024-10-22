import matplotlib.pyplot as plt
import numpy as np
import csv
from scipy.optimize import curve_fit

def load_data(filename):
    data = {'Time (s)': [], 'Potential 1 (V)': [], 'Potential 2 (V)': []}
    with open(filename, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)  # Skip header
        for row in csvreader:
            data['Time (s)'].append(float(row[0]))
            data['Potential 1 (V)'].append(float(row[2]))
            data['Potential 2 (V)'].append(float(row[3]))
    return data

def sine_wave(t, A, f, phi, offset):
    return A * np.sin(2 * np.pi * f * t + phi) + offset

def plot_data():
    data = load_data('data/10Hz-Sine.csv')
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    ax.plot(data['Time (s)'], data['Potential 1 (V)'], label='Potential 1')
    ax.plot(data['Time (s)'], data['Potential 2 (V)'], label='Potential 2')
    
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Potential (V)')
    ax.set_title('Potential 1 and Potential 2 vs Time')
    ax.legend()

    # Curve fitting
    t = np.array(data['Time (s)'])
    y1 = np.array(data['Potential 1 (V)'])
    y2 = np.array(data['Potential 2 (V)'])

    # Initial guess for parameters [A, f, phi, offset]
    p0 = [1.0, 10.0, 0.0, 0.0]

    # Fit both potentials
    popt1, _ = curve_fit(sine_wave, t, y1, p0=p0)
    popt2, _ = curve_fit(sine_wave, t, y2, p0=p0)

    # Plot fitted curves
    t_fit = np.linspace(t.min(), t.max(), 1000)
    ax.plot(t_fit, sine_wave(t_fit, *popt1), 'r--', label='Fit Potential 1')
    ax.plot(t_fit, sine_wave(t_fit, *popt2), 'g--', label='Fit Potential 2')

    # Calculate phase difference
    phase_diff = abs(popt1[2] - popt2[2])
    phase_diff_degrees = np.degrees(phase_diff) % 360

    ax.text(0.5, 0.95, f'Phase difference: {phase_diff_degrees:.2f}°', 
            transform=ax.transAxes, verticalalignment='top')

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    plot_data()

