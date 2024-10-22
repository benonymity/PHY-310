import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import linregress

# Read the CSV file
df = pd.read_csv('data/10Hz-Square-1s.csv')

# Dictionary to rename columns
column_rename = {
    'Latest: Time (s)': 'Time',
    'Latest: Potential 1 (V)': 'Inductor Voltage'
}

# Rename the columns
df = df.rename(columns=column_rename)

# Take the absolute value of the Inductor Voltage and calculate its natural logarithm
df['Inductor Voltage'] = np.abs(df['Inductor Voltage'])
df['ln(Inductor Voltage)'] = np.log(df['Inductor Voltage'])

# Function to find rising edges
def find_rising_edges(time, voltage, threshold=0.1):
    rising_edges = []
    for i in range(1, len(voltage)):
        if voltage[i] - voltage[i-1] > threshold:
            rising_edges.append(i-1)
    return rising_edges

# Find rising edges
rising_edges = find_rising_edges(df['Time'], df['Inductor Voltage'])

# Calculate slopes and plot fits
plt.figure(figsize=(12, 8))
plt.plot(df['Time'], df['ln(Inductor Voltage)'], label='ln(Inductor Voltage)')

slopes = []
for i, start in enumerate(rising_edges):
    end = start + 5  # Use 5 points for each rise
    x = df['Time'][start:end]
    y = df['ln(Inductor Voltage)'][start:end]
    
    slope, intercept, r_value, p_value, std_err = linregress(x, y)
    slopes.append(slope)
    
    # Plot fit line
    fit_line = slope * x + intercept
    plt.plot(x, fit_line, 'r--', label=f'Fit {i+1}, slope: {slope:.2f} 1/s')
    
    print(f"Slope of rise {i+1}: {slope:.2f} 1/s")

plt.xlabel('Time (s)')
plt.ylabel('ln(Absolute Voltage)')
plt.title('Natural Log of Absolute Inductor Voltage - 10Hz Square Wave with Fitted Lines')
plt.legend()
plt.grid(True)

# Save the plot as a PNG file
plt.savefig('images/ln_abs_inductor_voltage_square_with_fits.png')
plt.close()

# Calculate and print average slope
average_slope = np.mean(slopes)
print(f"Average slope: {average_slope:.2f} 1/s")

# Calculate inductance
resistance = 3.7  # Ohms
resistance_error = 0.1  # Ohms
voltage_error = 0.0001  # V

inductances = []
inductance_errors = []

for slope in slopes:
    inductance = -resistance / slope  # Note the negative sign here
    inductances.append(inductance)
    
    # Error propagation
    rel_error_R = resistance_error / resistance
    rel_error_slope = voltage_error / (slope * 0.0001)  # Assuming 0.0001s time resolution
    rel_error_L = np.sqrt(rel_error_R**2 + rel_error_slope**2)
    inductance_error = inductance * rel_error_L
    inductance_errors.append(inductance_error)

# Calculate average inductance and its error
average_inductance = np.mean(inductances)
average_inductance_error = np.sqrt(np.sum(np.array(inductance_errors)**2)) / len(inductances)

print(f"Average inductance: {average_inductance:.6f} ± {average_inductance_error:.6f} H")

# Create LaTeX table
latex_table = "\\begin{table}[h]\n\\centering\n\\begin{tabular}{|c|c|c|}\n\\hline\n"
latex_table += "Rise & Slope (1/s) & Inductance (H) \\\\\n\\hline\n"

for i, (slope, inductance, inductance_error) in enumerate(zip(slopes, inductances, inductance_errors)):
    latex_table += f"{i+1} & {slope:.2f} & {inductance:.6f} ± {inductance_error:.6f} \\\\\n"

latex_table += "\\hline\n"
latex_table += f"Average & {average_slope:.2f} & {average_inductance:.6f} ± {average_inductance_error:.6f} \\\\\n"
latex_table += "\\hline\n\\end{tabular}\n"
latex_table += "\\caption{Slopes and Calculated Inductances}\n\\label{tab:inductances}\n\\end{table}"

print("\nLaTeX Table:")
print(latex_table)

# Save LaTeX table to a file
with open('inductance_table.tex', 'w') as f:
    f.write(latex_table)
