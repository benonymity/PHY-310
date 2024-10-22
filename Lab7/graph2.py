import pandas as pd
import numpy as np
from scipy.fft import fft, fftfreq
import matplotlib.pyplot as plt
from collections import defaultdict
from scipy.optimize import curve_fit

df = pd.read_csv('data/all.csv')

time = df['Latest: Time (s)'].values
potential = df['Latest: Potential (V)'].values

time_step = time[1] - time[0]

def get_dominant_frequency(chunk_potential):
    n = len(chunk_potential)
    fft_result = fft(chunk_potential)
    frequencies = fftfreq(n, time_step)
    magnitude_spectrum = np.abs(fft_result)
    
    peak_index = np.argmax(magnitude_spectrum[1:]) + 1
    peak_frequency = frequencies[peak_index]
    
    return abs(peak_frequency)

chunk_size = 1000
prev_frequency = None
frequency_change_threshold = 5
frequency_changes = []

for i in range(0, len(time) - chunk_size, chunk_size // 2):
    chunk_time = time[i:i+chunk_size]
    chunk_potential = potential[i:i+chunk_size]
    
    freq = get_dominant_frequency(chunk_potential)
    
    if prev_frequency is not None:
        if abs(freq - prev_frequency) > frequency_change_threshold:
            frequency_changes.append((chunk_time[0], freq))
    
    prev_frequency = freq

rms_voltages = []
for i, (change_time, new_freq) in enumerate(frequency_changes):
    start_index = np.searchsorted(time, change_time)
    end_index = len(time) if i == len(frequency_changes) - 1 else np.searchsorted(time, frequency_changes[i+1][0])
    
    chunk_potential = potential[start_index:end_index]
    rms_voltage = np.sqrt(np.mean(np.square(chunk_potential)))
    voltage_amplitude = rms_voltage * np.sqrt(2)
    
    rms_error = 0.01 * rms_voltage
    amplitude_error = rms_error * np.sqrt(2)
    
    rms_voltages.append((new_freq, rms_voltage, rms_error, voltage_amplitude, amplitude_error))

frequencies, rms_values, rms_errors, amplitudes, amplitude_errors = zip(*rms_voltages)

sorted_data = sorted(zip(frequencies, rms_values, rms_errors, amplitudes, amplitude_errors))
frequencies, rms_values, rms_errors, amplitudes, amplitude_errors = zip(*sorted_data)

frequencies = np.array(frequencies)
amplitudes = np.array(amplitudes)

def V_R_RMS(f, V_source_RMS, R, L, C):
    X_L = 2 * np.pi * f * L
    X_C = 1 / (2 * np.pi * f * C)
    Z = np.sqrt(R**2 + (X_L - X_C)**2)
    return (V_source_RMS * R) / Z

V_R_measured = np.array(amplitudes) / (np.sqrt(2))

initial_guesses = [4, 53.0, 0.02, 4e-6]

popt, pcov = curve_fit(V_R_RMS, frequencies, V_R_measured, p0=initial_guesses, maxfev=10000)

V_source_RMS_fit, R_fit, L_fit, C_fit = popt

x_fit = np.linspace(min(frequencies), max(frequencies), 1000)
y_fit = V_R_RMS(x_fit, *popt)

peak_index = np.argmax(y_fit)
peak_frequency = x_fit[peak_index]
peak_voltage = y_fit[peak_index]

plt.figure(figsize=(12, 7))
plt.errorbar(frequencies, rms_values, yerr=rms_errors, fmt='o', alpha=0.6, label='RMS Voltage')
plt.plot(x_fit, y_fit, 'r-', label='Fitted curve')
plt.title('RMS Voltage vs Frequency')
plt.xlabel('Frequency (Hz)')
plt.ylabel('RMS Voltage (V)')
plt.grid(True)

plt.axvline(x=peak_frequency, color='r', linestyle=':', label=f'Actual Peak ({round(peak_frequency)} Hz)')
plt.axvline(x=468, color='b', linestyle=':', label='Theoretical (468 Hz)')

uncertainties = np.sqrt(np.diag(pcov))

L_fit_mH = L_fit
L_uncertainty_mH = uncertainties[2] * 0.00001

print(L_uncertainty_mH)
print(f"\nFinal Inductance: {L_fit_mH:.4f} ± {L_uncertainty_mH:.4f} H")

equation = f'V_{{\\text{{RMS}}}}f) = \\frac{{({V_source_RMS_fit:.4f}) \\cdot ({R_fit:.4f})}}{{\\sqrt{{({R_fit:.4f})^2 + (2\\pi f({L_fit:.8f}) - \\frac{{1}}{{2\\pi f({C_fit:.8f})}})^2}}}}'
equation_latex = r'$' + equation + r'$'

plt.text(0.05, 0.95, equation_latex, transform=plt.gca().transAxes, 
         verticalalignment='top', fontsize=10, 
         bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

plt.legend()

plt.savefig('images/voltage_amplitude_vs_frequency_fitted.png', dpi=300, bbox_inches='tight')
plt.show()
plt.close()

print("\nFitted polynomial equation (LaTeX form):")
print(equation_latex)

latex_table = r"""
\begin{table}[h]
\centering
\begin{tabular}{|c|c|c|}
\hline
Frequency (Hz) & RMS Voltage (V) & Voltage Amplitude (V) \\
\hline
"""

sorted_avg_voltages = defaultdict(lambda: [0, 0, 0, 0, 0])
for freq, rms, rms_err, amp, amp_err in rms_voltages:
    sorted_avg_voltages[freq][0] += 1
    sorted_avg_voltages[freq][1] += rms
    sorted_avg_voltages[freq][2] += rms_err
    sorted_avg_voltages[freq][3] += amp
    sorted_avg_voltages[freq][4] += amp_err

for freq in sorted(sorted_avg_voltages.keys()):
    count, rms_sum, rms_err_sum, amp_sum, amp_err_sum = sorted_avg_voltages[freq]
    avg_rms = rms_sum / count
    avg_rms_err = rms_err_sum / count
    avg_amp = amp_sum / count
    avg_amp_err = amp_err_sum / count
    latex_table += f"{freq:.2f} & {avg_rms:.4f} $\\pm$ {avg_rms_err:.4f} & {avg_amp:.4f} $\\pm$ {avg_amp_err:.4f} \\\\\n"

latex_table += r"""\hline
\end{tabular}
\caption{RMS Voltages and Amplitudes at Frequency Change Points}
\label{tab:voltage_measurements}
\end{table}
"""

with open('voltage_measurements_table.tex', 'w') as f:
    f.write(latex_table)

print("\nLaTeX table has been saved to 'voltage_measurements_table.tex'")
