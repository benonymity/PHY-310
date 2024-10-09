import os
import pandas as pd
import numpy as np

def get_peaks_with_error(file_path):
    df = pd.read_csv(file_path, skiprows=[0])
    results = {
        'Peak EMF (mV)': (np.max(np.abs(df.iloc[:, 1])), 0.001),
        'Peak Voltage (V)': (np.max(np.abs(df.iloc[:, 2])), 0.001),
        'Peak Current (A)': (np.max(np.abs(df.iloc[:, 3])), 0.001)
    }
    return results

data_folder = 'data'
csv_files = sorted([f for f in os.listdir(data_folder) if f.endswith('.csv')])

all_results = []

for file in csv_files:
    file_path = os.path.join(data_folder, file)
    file_results = get_peaks_with_error(file_path)
    file_results['File'] = file
    all_results.append(file_results)

results_df = pd.DataFrame(all_results)

results_df['Frequency (Hz)'] = results_df['File'].str.extract(r'(\d+)').astype(int)

results_df = results_df.sort_values('Frequency (Hz)')

results_df['Resistance $\Omega$'] = results_df['Peak Voltage (V)'].apply(lambda x: x[0] / results_df['Peak Current (A)'].iloc[0][0])
results_df['Resistance Error'] = results_df['Resistance $\Omega$'] * np.sqrt(
    (results_df['Peak Voltage (V)'].apply(lambda x: x[1] / x[0]))**2 +
    (results_df['Peak Current (A)'].apply(lambda x: x[1] / x[0]))**2
)

def calculate_turns(row):
    peak_emf, peak_emf_error = row['Peak EMF (mV)']
    peak_current, peak_current_error = row['Peak Current (A)']
    frequency = row['Frequency (Hz)']
    
    pi = np.pi
    r = 0.0022
    mu = 0.868
    
    n = peak_emf * 0.001 / (2 * pi**2 * r**2 * peak_current * frequency * mu)
    
    relative_error = np.sqrt((peak_emf_error/peak_emf)**2 + (peak_current_error/peak_current)**2)
    n_error = n * relative_error
    
    return n, n_error

results_df['Turns'] = results_df.apply(calculate_turns, axis=1)

results_df['Turns'] = results_df['Turns'].apply(lambda x: f'{x[0]:.4f} ± {x[1]:.4f}')

for col in ['Peak EMF (mV)', 'Peak Voltage (V)', 'Peak Current (A)', 'Resistance $\Omega$']:
    if col != 'Resistance $\Omega$':
        results_df[col] = results_df[col].apply(lambda x: f'{x[0]:.4f} ± {x[1]:.4f}')
    else:
        results_df[col] = results_df.apply(lambda row: f'{row[col]:.4f} ± {row["Resistance Error"]:.4f}', axis=1)

results_df = results_df.drop('Resistance Error', axis=1)

cols = ['File', 'Frequency (Hz)'] + [col for col in results_df.columns if col not in ['File', 'Frequency (Hz)']]
results_df = results_df[cols]

results_df = results_df.drop('File', axis=1)

results_df['Frequency (Hz)'] = results_df['Frequency (Hz)'].astype(str) + ' Hz'

print(results_df.to_string(index=False))

df1 = results_df[['Frequency (Hz)', 'Peak Voltage (V)', 'Peak Current (A)', 'Resistance $\Omega$']]
df2 = results_df[['Frequency (Hz)', 'Peak EMF (mV)', 'Peak Current (A)', 'Turns']]

latex_table1 = df1.to_latex(index=False, escape=False, column_format='|l|l|l|l|')
latex_table2 = df2.to_latex(index=False, escape=False, column_format='|l|l|l|l|')

latex_output = f"""
\\begin{{table}}[]
\\centering
\\begin{{tabular}}{{|l|l|l|l|}}
\\hline
{latex_table1.split('\\toprule', 1)[1].split('\\bottomrule', 1)[0].strip().replace('\\\\', '\\\\ \\hline').replace("\\midrule\n", "")}
\\end{{tabular}}
\\caption{{Peak values of frequency, voltage, current, and resistance}}
\\label{{tab:peak_values1}}
\\end{{table}}

\\begin{{table}}[]
\\centering
\\begin{{tabular}}{{|l|l|l|l|}}
\\hline
{latex_table2.split('\\toprule', 1)[1].split('\\bottomrule', 1)[0].strip().replace('\\\\', '\\\\ \\hline').replace("\\midrule\n", "")}
\\end{{tabular}}
\\caption{{Peak values of frequency, EMF, current, and number of turns}}
\\label{{tab:peak_values2}}
\\end{{table}}
"""

with open('peak_values_tables.tex', 'w') as f:
    f.write(latex_output)

print("LaTeX tables have been saved to 'peak_values_tables.tex'")

turns_1_to_9_hz = results_df[results_df['Frequency (Hz)'].str.contains('1 Hz|2 Hz|3 Hz|4 Hz|5 Hz|6 Hz|7 Hz|8 Hz|9 Hz')]['Turns']

turns_values = [float(t.split('±')[0]) for t in turns_1_to_9_hz]
turns_errors = [float(t.split('±')[1]) for t in turns_1_to_9_hz]

avg_turns = sum(turns_values) / len(turns_values)

propagated_error = (sum([e**2 for e in turns_errors]) / len(turns_errors))**0.5

print(f"\nAverage number of turns from 1-9 Hz: {avg_turns:.4f} ± {propagated_error:.4f}")

