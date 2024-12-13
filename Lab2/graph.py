import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

# Define your data here
area = [13, 50, 113, 201, 314]  # List for area values (x-axis)
b_value1 = [0.4248, 1.374, 3.300, 5.588, 9.900]  # Oscillation damping constants (y-axis)
b_value2 = [0.4238, 1.736, 4.760, 8.028, 14.13]  # Envelope damping constants (y-axis)

# Define error values (± 0.2 for each damping constant)
b_value1_error = [0.2] * len(b_value1)
b_value2_error = [0.2] * len(b_value2)

# Define linear function for fitting
def linear(x, m, b):
    return m * x + b

# Fit the data with error weights
popt1, pcov1 = curve_fit(linear, area, b_value1, sigma=b_value1_error, absolute_sigma=True)
popt2, pcov2 = curve_fit(linear, area, b_value2, sigma=b_value2_error, absolute_sigma=True)

# Create two separate plots
for i, (b_value, b_error, popt, pcov, title, color) in enumerate([
    (b_value1, b_value1_error, popt1, pcov1, 'Oscillation Damping Constant', 'blue'),
    (b_value2, b_value2_error, popt2, pcov2, 'Envelope Damping Constant', 'red')
]):
    plt.figure(figsize=(10, 6))
    
    # Plot scatter with error bars
    plt.errorbar(area, b_value, yerr=b_error, color=color, fmt='o', label=title, capsize=5)

    # Plot fitted line
    x_fit = np.linspace(min(area), max(area), 100)
    plt.plot(x_fit, linear(x_fit, *popt), ':', color=color, label='Fitted Line')

    # Set labels for axes
    plt.xlabel('Area (cm$^2$)')
    plt.ylabel('Damping constant')

    # Add legend
    plt.legend()

    # Add grid lines for better readability
    plt.grid(True, linestyle='--', alpha=0.7)

    # Calculate standard errors from covariance matrix
    perr = np.sqrt(np.diag(pcov))

    # Display equation in LaTeX format with error
    eq = f'$y = ({popt[0]:.4f} \\pm {perr[0]:.4f})x {popt[1]:+.4f} \\pm {perr[1]:.4f}$'
    plt.text(0.5, 0.95, eq, transform=plt.gca().transAxes, fontsize=12, 
             verticalalignment='top', horizontalalignment='center',
             bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

    # Set title
    plt.title(title)

    # Adjust layout to prevent cutting off labels
    plt.tight_layout()

    # Save the plot as a PNG file
    plt.savefig(f'images/b-area_{title.lower().replace(" ", "_")}.png', dpi=300, bbox_inches='tight')

    # Display the plot
    plt.show()
