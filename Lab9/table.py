import numpy as np

lens_data = [
    {"f": 25.0, "position": 12.0, "do": 12.0, "position_err": 0.1},
    {"f": 20.0, "position": 20.0, "position_err": 0.1},
    {"f": -15.0, "position": 54.0, "position_err": 0.1},
    {"f": -15.0, "position": 84.0, "position_err": 0.1}
]

source_position = 0.0
screen_position = 106.0

def calculate_image_distance(f, do):
    return 1 / (1 / f - 1 / do)

def calculate_magnification(di, do):
    return -di / do

def calculate_magnification_error(di, di_err, do, do_err):
    rel_err_di = di_err / abs(di)
    rel_err_do = do_err / abs(do)
    rel_err_total = np.sqrt(rel_err_di**2 + rel_err_do**2)
    return abs(di/do) * rel_err_total

def calculate_image_distance_error(f, do, do_err):
    partial_do = 1 / (do**2 * (1/f - 1/do)**2)
    return abs(partial_do * do_err)

magnifications = []
total_magnification = 1.0
total_mag_error = 0.0

previous_position = source_position
previous_di = 0
previous_di_err = 0

for i, lens in enumerate(lens_data):
    if i == 0:
        do = lens["do"]
        do_err = lens["position_err"]
    else:
        do = lens["position"] - (previous_position + previous_di)
        do_err = np.sqrt(lens["position_err"]**2 + previous_di_err**2)
        
    di = calculate_image_distance(lens["f"], do)
    di_err = calculate_image_distance_error(lens["f"], do, do_err)
    
    mag = calculate_magnification(di, do)
    mag_err = calculate_magnification_error(di, di_err, do, do_err)
    
    magnifications.append((mag, mag_err, di, di_err))
    total_magnification *= mag
    if total_mag_error == 0:
        total_mag_error = mag_err/abs(mag)
    else:
        total_mag_error = np.sqrt((total_mag_error)**2 + (mag_err/abs(mag))**2)
    
    previous_position = lens["position"]
    previous_di = di
    previous_di_err = di_err

final_image_distance = screen_position - (previous_position + previous_di)
final_image_distance_err = np.sqrt(previous_di_err**2 + lens_data[-1]["position_err"]**2)

total_mag_error = abs(total_magnification) * total_mag_error

table = r"""
\begin{table}[h]
\centering
\begin{tabular}{|c|c|c|c|c|}
\hline
Lens & Position (cm) & Focal Length (cm) & Image Distance (cm) & Magnification \\
\hline
"""

for i, (mag, mag_err, di, di_err) in enumerate(magnifications):
    table += f"{i+1} & {lens_data[i]['position']:.1f} ± {lens_data[i]['position_err']:.1f} & {lens_data[i]['f']:.1f} & {di:.3f} ± {di_err:.3f} & {mag:.3f} ± {mag_err:.3f} \\\\\n"

table += r"""
\hline
\multicolumn{4}{|c|}{Total Magnification} & """ + f"{total_magnification:.3f} ± {total_mag_error:.3f} \\\\\n"

table += r"""
\hline
\multicolumn{4}{|c|}{Final Image Distance (cm)} & """ + f"{final_image_distance:.3f} ± {final_image_distance_err:.3f} \\\\\n"

table += r"""
\hline
\end{tabular}
\caption{Lens positions, focal lengths, image distances, and magnifications}
\label{tab:lens_system}
\end{table}
"""

print(table)
with open('table.tex', 'w') as file:
    file.write(table)
