import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

# Define your data here
area = [13, 50, 113, 201, 314]  # List for area values (x-axis)
b_value1 = [0.4248, 1.374, 3.300, 5.588, 9.900]  # Oscillation damping constants (y-axis)
b_value2 = [0.4238, 1.736, 4.760, 8.028, 14.13]  # Envelope damping constants (y-axis)

# Define linear function for fitting
def linear(x, m, b):
    return m * x + b

# Fit the data
popt1, _ = curve_fit(linear, area, b_value1)
popt2, _ = curve_fit(linear, area, b_value2)

# Create two separate plots
for i, (b_value, popt, title, color) in enumerate([
    (b_value1, popt1, 'Oscillation Damping Constant', 'blue'),
    (b_value2, popt2, 'Envelope Damping Constant', 'red')
]):
    plt.figure(figsize=(10, 6))
    plt.scatter(area, b_value, color=color, label=title)

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

    # Display equation in LaTeX format
    eq = f'$y = {popt[0]:.4f}x {popt[1]:+.4f}$'
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
