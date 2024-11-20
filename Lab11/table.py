import numpy as np
import pandas as pd

# Constants
mag = 4.3 # Magnification factor
S = 26e9  # Glass shear modulus (Pa)
wavelength = 650e-9  # Wavelength of light (m)
ell = 0.00015  # Thickness of the slide (m)
area_error = 0.001  # Error in area measurement (cm^2)

# Measured areas (cm^2)
# areas_cm2 = np.array([2.846, 2.665, 2.667]) # Old ellipse fitting
areas_cm2 = np.array([1.137, 1.150, 1.060])
areas_corrected = areas_cm2 / mag 
areas_m2 = areas_corrected * 1e-4  # Convert from cm^2 to m^2
area_errors_m2 = area_error / mag * 1e-4  # Convert error to m^2

# Calculate average radius and area
average_area = np.mean(areas_m2)
area_error_avg = np.sqrt(np.sum(area_errors_m2**2)) / len(areas_m2)

# Calculate individual forces and errors
forces = S * areas_m2 * wavelength / (2 * ell)
force_errors = S * wavelength * area_errors_m2 / (2 * ell)

# Calculate force using F = (S*A*λ)/(2*ℓ)
average_force = S * average_area * wavelength / (2 * ell)
average_force_error = S * wavelength * area_error_avg / (2 * ell)

# Prepare data for display
data = {
    "Corrected Area (cm^2)": areas_corrected,
    "Force (N)": forces,
    "Force Error (N)": force_errors,
}

results = pd.DataFrame(data)

# Print results
print("\nNewton's Rings Force Calculation Results:")
print("Ring | Area (cm²) | Force (N)")
print("-" * 45)
for i, row in results.iterrows():
    print(f"{i+1} | {row['Corrected Area (cm^2)']:.3f} ± {area_error:.3f} | {row['Force (N)']:.2f} ± {row['Force Error (N)']:.2f}")
print("-" * 45)
print(f"Average Force: {average_force:.2f} ± {average_force_error:.2f} N")

# Create table
latex_table = """\\begin{table}[h]
\\centering
\\begin{tabular}{|c|c|c|}
\\hline
Ring & Area (cm$^2$) & Force (N) \\\\
\\hline"""

for i, row in results.iterrows():
    latex_table += f"\n{i+1} & {row['Corrected Area (cm^2)']:.3f} ± {area_error:.3f} & {row['Force (N)']:.2f} ± {row['Force Error (N)']:.2f} \\\\"

latex_table += f"""
\\hline
\\multicolumn{{2}}{{|c|}}{{Average Force}} & {average_force:.2f} ± {average_force_error:.2f} N \\\\
\\hline
\\end{{tabular}}
\\caption{{Force Calculations}}
\\label{{tab:force_results}}
\\end{{table}}"""

# Write to file
with open('table.tex', 'w') as f:
    f.write(latex_table)
