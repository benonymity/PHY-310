import numpy as np

# Data
n = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
frequency = np.array([12.4, 24.6, 35.6, 44.2, 57.9, 64.7, 73.4, 75.5, 79.8])
frequency_error = 0.1
wavelength = np.array([100, 50, 33, 25, 20, 17, 14, 13, 11])
wavelength_error = 1

# Convert wavelength to meters
wavelength = 2 * wavelength / 100
wavelength_error = wavelength_error / 100

# Calculate velocity
velocity = wavelength * frequency
velocity_error = np.sqrt((frequency * wavelength_error)**2 + (wavelength * frequency_error)**2)

# Calculate angular wave number
k = 2 * np.pi / wavelength
k_error = 2 * np.pi * wavelength_error / (wavelength**2)

# Calculate angular frequency
omega = velocity * k
omega_error = np.sqrt((k * velocity_error)**2 + (velocity * k_error)**2)

# Generate LaTeX table
print("\\begin{table}[]")
print("\\centering")
print("\\begin{tabular}{|l|l|l|l|l|l|}")
print("\\hline")
print("      & Frequency     & Wavelength $\\lambda$ & Velocity & Angular Wave Number $k$ & Angular Frequency $\\omega$ \\\\ \\hline")

for i in range(9):
    print(f"$n={n[i]}$ & {frequency[i]:.1f} ± {frequency_error:.1f} Hz & {wavelength[i]*100:.0f} ± 1 cm & {velocity[i]:.2f} ± {velocity_error[i]:.2f} m/s & {k[i]:.2f} ± {k_error[i]:.2f} m$^{{-1}}$ & {omega[i]:.2f} ± {omega_error[i]:.2f} rad/s \\\\ \\hline")

print("\\end{tabular}")
print("\\caption{Calculated values for different modes}")
print("\\label{tab:calculated-values}")
print("\\end{table}")

# Output angular frequency and wave number as lists
print("\nAngular Frequency (omega) list:")
print([f"{omega[i]:.2f}" for i in range(len(omega))])

print("\nAngular Wave Number (k) list:")
print([f"{k[i]:.2f}" for i in range(len(k))])
