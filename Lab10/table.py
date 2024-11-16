import numpy as np
import matplotlib.pyplot as plt

# Data with uncertainties
distances = np.array([10, 20, 30, 40, 50, 60, 70, 80, 90, 100])  # cm
distances_err = np.full_like(distances, 0.1)  # cm

beam_widths = np.array([2.5, 3, 3.5, 4, 5, 6.5, 8, 9.5, 11.5, 13])  # mm
beam_widths_err = np.full_like(beam_widths, 0.3)  # mm

# Calculate diameters and uncertainties
wavelength = 650e-9 
distances_m = distances / 100
beam_widths_m = beam_widths / 1000

diameters = (2 * wavelength * distances_m) / beam_widths_m
diameters_mm = diameters * 1000

# Error propagation
rel_err_dist = distances_err / distances
rel_err_width = beam_widths_err / beam_widths
rel_err_total = np.sqrt(rel_err_dist**2 + rel_err_width**2)
diameter_errs = diameters * rel_err_total
diameter_errs_mm = diameter_errs * 1000 

# Create LaTeX table
table = r"""
\begin{table}[h]
\centering
\begin{tabular}{|c|c|c|c|}
\hline
Distance (cm) & Beam Width (mm) & Diameter (mm) \\
\hline
"""

for d, d_err, w, w_err, diam, diam_err in zip(distances, distances_err, 
                                             beam_widths, beam_widths_err,
                                             diameters_mm, diameter_errs_mm):
    table += f"{d:.1f} ± {d_err:.1f} & {w:.1f} ± {w_err:.1f} & {diam:.3f} ± {diam_err:.3f} \\\\\n"

# Calculate average of last 8 points
avg_diameter = np.mean(diameters_mm[-8:])
avg_err = np.sqrt(np.sum(diameter_errs_mm[-8:]**2))/8

table += r"\hline" + "\n"
table += r"\multicolumn{2}{|c|}{Average of last 8 diameters} & " + f"{avg_diameter:.3f} ± {avg_err:.3f} \\\\\n"

table += r"""\hline
\end{tabular}
\caption{Beam width measurements and calculated diameters}
\label{tab:beam_measurements}
\end{table}
"""

# Create plot
import matplotlib.font_manager as font_manager

font_path = '/Users/benbassett/Developer/PHY-310/Lab10/Wingdings2.ttf'
font_manager.fontManager.addfont(font_path)
prop = font_manager.FontProperties(fname=font_path, family='Wingdings 3')

plt.rcParams['font.family'] = 'Wingdings 3'
plt.rcParams['font.fantasy'] = prop.get_name()
# plt.rcParams['font.family'] = 'Wingdings'
plt.figure(figsize=(10, 6))
plt.errorbar(distances, diameters_mm, 
            xerr=distances_err, yerr=diameter_errs_mm,
            fmt='o', capsize=5, label='Data with uncertainties')

plt.xlabel('Distance (cm)')
plt.ylabel('Diameter (mm)')
plt.title('Beam Diameter vs Distance')
plt.grid(True)
plt.legend()

plt.savefig('beam_diameter.png')
plt.close()

# Save table to file
with open('beam_table.tex', 'w') as f:
    f.write(table)
