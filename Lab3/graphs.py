import matplotlib.pyplot as plt
import numpy as np

# Example data
number_of_nodes = [1, 2, 3, 4, 5, 6]
frequency = [13.67, 26.48, 40.54, 54.58, 68.37, 82.07]
amplitude = [21, 9.5, 8, 5.5, 3.5, 2.5]

# Fit to a line for frequency
coefficients_freq = np.polyfit(number_of_nodes, frequency, 1)
polynomial_freq = np.poly1d(coefficients_freq)
line_fit_freq = polynomial_freq(number_of_nodes)

# Calculate R^2 for frequency
residuals_freq = frequency - line_fit_freq
ss_res_freq = np.sum(residuals_freq**2)
ss_tot_freq = np.sum((frequency - np.mean(frequency))**2)
r_squared_freq = 1 - (ss_res_freq / ss_tot_freq)

# Plotting the frequency data
plt.figure(figsize=(10, 6))
plt.plot(number_of_nodes, frequency, marker='o', linestyle='-', color='b', label='Frequency vs Number of Nodes')
plt.plot(number_of_nodes, line_fit_freq, linestyle='--', color='r', label=f'Fit: y={coefficients_freq[0]:.2f}x+{coefficients_freq[1]:.2f}, $R^2$={r_squared_freq:.2f}')
plt.xlabel('Number of Nodes ($n$)')
plt.ylabel('Frequency (Hz)')
plt.title('Frequency vs Number of Nodes')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig('frequency1-6.png')
plt.show()

# Fit to an exponential for amplitude
def exponential_fit(x, a, b):
    return a * np.exp(b * x)

# Initial guess for the parameters
initial_guess = [1, 0.1]

# Perform the exponential fit
params = np.polyfit(number_of_nodes, np.log(amplitude), 1, w=np.sqrt(amplitude))
a = np.exp(params[1])
b = params[0]
line_fit_amp = exponential_fit(np.array(number_of_nodes), a, b)

# Calculate R^2 for amplitude
residuals_amp = amplitude - line_fit_amp
ss_res_amp = np.sum(residuals_amp**2)
ss_tot_amp = np.sum((amplitude - np.mean(amplitude))**2)
r_squared_amp = 1 - (ss_res_amp / ss_tot_amp)

# Plotting the amplitude data
plt.figure(figsize=(10, 6))
plt.plot(number_of_nodes, amplitude, marker='o', linestyle='-', color='b', label='Amplitude vs Number of Nodes')
# plt.plot(number_of_nodes, line_fit_amp, linestyle='--', color='r', label=f'Fit: y={a:.2f}e^({b:.2f}x), $R^2$={r_squared_amp:.2f}')
plt.xlabel('Number of Nodes ($n$)')
plt.ylabel('Amplitude (mm)')
plt.title('Amplitude vs Number of Nodes')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig('amplitude1-6.png')
plt.show()

# Data for tension vs frequency
tension = np.array([0.343, 0.981, 1.47, 1.96, 2.45, 2.94, 3.29])
frequency = np.array([26.48, 45.48, 55.58, 65.60, 73.64, 80.93, 84.93])

# Wavelength is constant
wavelength = 0.76  # in meters

# Fit a model to the data based on the equation v = sqrt(tension) / constant
def model(tension, constant):
    return (1 / wavelength) * np.sqrt(tension) / np.sqrt(constant)

# Initial guess for the constant
initial_guess = [1]

# Perform the fit
from scipy.optimize import curve_fit
params, covariance = curve_fit(model, tension, frequency, p0=initial_guess)
fitted_constant = params[0]

# Calculate the fitted line
line_fit_tension_freq = model(tension, fitted_constant)

# Calculate R^2 for the fit
residuals_tension_freq = frequency - line_fit_tension_freq
ss_res_tension_freq = np.sum(residuals_tension_freq**2)
ss_tot_tension_freq = np.sum((frequency - np.mean(frequency))**2)
r_squared_tension_freq = 1 - (ss_res_tension_freq / ss_tot_tension_freq)

# Plotting the tension vs frequency data
plt.figure(figsize=(10, 6))
plt.plot(tension, frequency, marker='o', linestyle='-', color='b', label='Frequency vs Tension')
plt.plot(tension, line_fit_tension_freq, linestyle='--', color='r', label=f'Fit: $f=\\frac{{1}}{{{wavelength}}}\\sqrt{{\\frac{{T}}{{{fitted_constant:2f}}}}}$, $R^2$={r_squared_tension_freq:.2f}')
plt.xlabel('Tension (N)')
plt.ylabel('Frequency (Hz)')
plt.title('Frequency vs Tension')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig('tension_vs_frequency.png')
plt.show()

velocity = np.array([209.2, 209.7, 209.8, 209.0, 209.2, 209.3])  # Corrected typo in last value

# Fit to a line for velocity
coefficients_vel = np.polyfit(number_of_nodes, velocity, 1)
polynomial_vel = np.poly1d(coefficients_vel)
line_fit_vel = polynomial_vel(number_of_nodes)

# Calculate R^2 for velocity
residuals_vel = velocity - line_fit_vel
ss_res_vel = np.sum(residuals_vel**2)
ss_tot_vel = np.sum((velocity - np.mean(velocity))**2)
r_squared_vel = 1 - (ss_res_vel / ss_tot_vel)

# Plotting the velocity data
plt.figure(figsize=(10, 6))
plt.plot(number_of_nodes, velocity, marker='o', linestyle='-', color='b', label='Velocity vs Number of Nodes')
plt.plot(number_of_nodes, line_fit_vel, linestyle='--', color='r', label=f'Fit: y={coefficients_vel[0]:.2f}x+{coefficients_vel[1]:.2f}, $R^2$={r_squared_vel:.2f}')
plt.xlabel('Number of Nodes ($n$)')
plt.ylabel('Velocity (m/s)')
plt.title('Velocity vs Number of Nodes')
plt.ylim(0, 300)  # Set y-axis limits from 0 to 300
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig('velocity_vs_nodes.png')
plt.show()