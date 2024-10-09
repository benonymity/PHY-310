import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

data = pd.read_csv('B-E fields.csv')

voltage = data['V']
amps = data['Amps']
mtesla = data['mTesla']

slope_i, intercept_i, r_value_i, p_value_i, std_err_i = stats.linregress(amps, mtesla)

plt.figure(figsize=(10, 6))

plt.scatter(amps, mtesla, color='blue', label='Data')

fit_line_i = slope_i * amps + intercept_i
equation_i = f'$B(I) = {slope_i:.4f} \\cdot I + {intercept_i:.4f}$'
plt.plot(amps, fit_line_i, color='red', label='Fitted Line: ' + equation_i)

plt.xlabel('Current (Amps)')
plt.ylabel('Magnetic Field (mTesla)')
plt.title('Relationship between Current and Magnetic Field')

plt.legend()
plt.grid(True)

plt.tight_layout()
plt.savefig('Current_vs_Magnetic_Field.png')
plt.show()

print("Current vs Magnetic Field:")
print(f"Slope: {slope_i:.6f} mTesla/Amp")
print(f"Intercept: {intercept_i:.6f} mTesla")
print(f"R-squared: {r_value_i**2:.6f}")
print(f"Standard Error: {std_err_i:.6f}")

slope_v, intercept_v, r_value_v, p_value_v, std_err_v = stats.linregress(voltage, mtesla)

plt.figure(figsize=(10, 6))

plt.scatter(voltage, mtesla, color='green', label='Data')

fit_line_v = slope_v * voltage + intercept_v
equation_v = f'$B(V) = {slope_v:.4f} \\cdot V + {intercept_v:.4f}$'
plt.plot(voltage, fit_line_v, color='orange', label='Fitted Line: ' + equation_v)

plt.xlabel('Voltage (V)')
plt.ylabel('Magnetic Field (mTesla)')
plt.title('Relationship between Voltage and Magnetic Field')

plt.legend()
plt.grid(True)

plt.tight_layout()
plt.savefig('Voltage_vs_Magnetic_Field.png')
plt.show()

print("\nVoltage vs Magnetic Field:")
print(f"Slope: {slope_v:.6f} mTesla/V")
print(f"Intercept: {intercept_v:.6f} mTesla")
print(f"R-squared: {r_value_v**2:.6f}")
print(f"Standard Error: {std_err_v:.6f}")
