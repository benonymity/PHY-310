import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

# Data from the table
nodes = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
frequency = np.array([12.4, 24.6, 35.6, 44.2, 57.9, 64.7, 73.4, 75.5, 79.8])
frequency_error = 3 

# Define the function for curve fitting (square root function)
def fit_function(x, a, b):
    return a * np.sqrt(x) + b

# Perform curve fitting
popt, pcov = curve_fit(fit_function, nodes, frequency)

# Generate points for the fitted curve
x_fit = np.linspace(min(nodes), max(nodes), 100)
y_fit = fit_function(x_fit, *popt)

# Calculate R-squared
residuals = frequency - fit_function(nodes, *popt)
ss_res = np.sum(residuals**2)
ss_tot = np.sum((frequency - np.mean(frequency))**2)
r_squared = 1 - (ss_res / ss_tot)

# Create the plot
plt.figure(figsize=(10, 6))
plt.errorbar(nodes, frequency, yerr=frequency_error, fmt='o', color='blue', label='Frequency data', capsize=5)
plt.plot(x_fit, y_fit, 'r-', label=f'Fit: y = {popt[0]:.2f}√x + {popt[1]:.2f}')

# Add labels and title
plt.xlabel('Number of Nodes (n)')
plt.ylabel('Frequency (Hz)')
plt.title('Frequency vs Number of Nodes')

# Add grid
plt.grid(True, linestyle='--', alpha=0.7)

# Add legend with R-squared value
plt.legend(title=f'R² = {r_squared:.4f}')

# Ensure integer ticks for nodes
plt.xticks(nodes)

# Adjust layout and save the figure
plt.tight_layout()
plt.savefig('images/frequency_vs_nodes.png')
plt.show()

