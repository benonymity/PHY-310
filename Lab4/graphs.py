import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from sklearn.metrics import r2_score

# Data from the table
angular_wave_number = np.array([3.14, 6.28, 9.52, 12.57, 15.71, 18.48, 22.44, 24.17, 28.56])
angular_frequency = np.array([77.91, 154.57, 223.68, 277.72, 363.80, 406.52, 461.19, 474.38, 501.40])

# Error values from the table
angular_wave_number_error = np.array([0.02, 0.06, 0.14, 0.25, 0.39, 0.54, 0.80, 0.93, 1.30])
angular_frequency_error = np.array([0.84, 2.27, 4.83, 7.88, 12.88, 16.92, 23.30, 25.81, 32.24])

def fitted_function(k, A, B):
    return 2 * A * np.sin(B * k / 2)

# Constants
a = 0.1  # meters (given)
m = 0.001  # kilograms (changed)
T = 5.935  # newtons (changed)

# Calculate k_max
k_max = np.pi / a

# Filter data points within the range [0, pi/a]
mask = angular_wave_number <= k_max
angular_wave_number_filtered = angular_wave_number[mask]
angular_frequency_filtered = angular_frequency[mask]
angular_wave_number_error_filtered = angular_wave_number_error[mask]
angular_frequency_error_filtered = angular_frequency_error[mask]

# Fit the function to the filtered data
popt, _ = curve_fit(fitted_function, angular_wave_number_filtered, angular_frequency_filtered)
A_fit, B_fit = popt

# Print the fitted parameters
print(f"Fitted parameters: A = {A_fit:.4f}, B = {B_fit:.4f}")

# Theoretical function
def theoretical_function(k, T, m, a):
    return 2 * np.sqrt(T / (m * a)) * np.sin((k * a) / 2)

# Generate points for theoretical and fitted curves
k_fit = np.linspace(0, k_max, 100)
omega_theoretical = theoretical_function(k_fit, T, m, a)
omega_fitted = fitted_function(k_fit, A_fit, B_fit)

# Calculate R^2 for theoretical curve
omega_theoretical_data = theoretical_function(angular_wave_number_filtered, T, m, a)
r2_theoretical = r2_score(angular_frequency_filtered, omega_theoretical_data)

# Calculate R^2 for fitted curve
omega_fitted_data = fitted_function(angular_wave_number_filtered, A_fit, B_fit)
r2_fitted = r2_score(angular_frequency_filtered, omega_fitted_data)

# Create the plot
plt.figure(figsize=(10, 6))
plt.errorbar(angular_wave_number_filtered, angular_frequency_filtered, 
             xerr=angular_wave_number_error_filtered, yerr=angular_frequency_error_filtered, 
             fmt='o', color='blue', label='Data', capsize=5, ecolor='gray', elinewidth=1)
plt.plot(k_fit, omega_theoretical, 'r-', label=f'Theoretical: $\\omega = 2\\sqrt{{\\frac{{T}}{{ma}}}} \\sin(\\frac{{ka}}{{2}})$ (R² = {r2_theoretical:.4f})')
# plt.plot(k_fit, omega_fitted, 'g--', label=f'Fitted: $\\omega = 2A \\sin(\\frac{{Bk}}{{2}})$ (R² = {r2_fitted:.4f})')

# Add labels and title
plt.xlabel('Angular Wave Number (k) [rad/m]')
plt.ylabel('Angular Frequency (ω) [rad/s]')
plt.title('Dispersion Relation: Angular Frequency vs Angular Wave Number')

# Set x-axis limit from 0 to pi/a
plt.xlim(0, k_max)

# Add grid
plt.grid(True, linestyle='--', alpha=0.7)

# Add legend
plt.legend()

# Adjust layout and save the figure
plt.tight_layout()
plt.savefig('images/dispersion_relation_filtered_with_errors.png')
plt.show()

print(f"Theoretical parameters: T = {T} N, m = {m} kg, a = {a} m")
print(f"R² for theoretical curve: {r2_theoretical:.4f}")
print(f"R² for fitted curve: {r2_fitted:.4f}")
