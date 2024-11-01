import numpy as np

# Distance measurements in meters with uncertainty of 0.1m
distance = np.array([30, 16, 22, 14.3, 12.8, 18, 14, 9, 16])
distance_uncertainty = 0.1

# Calculate frequencies and their uncertainties
c = 299792458  # Speed of light in m/s
lambda_m = 0.01  # Wavelength in meters

frequency = c/(distance * lambda_m)
# Error propagation formula: df/dd = -c/(d^2 * lambda)
frequency_uncertainty = np.abs(-c/(distance**2 * lambda_m) * distance_uncertainty)

print("Distances:")
print("30.0 ± 0.1 m")
print("16.0 ± 0.1 m") 
print("22.0 ± 0.1 m")
print("14.3 ± 0.1 m")
print("12.8 ± 0.1 m")
print("18.0 ± 0.1 m")
print("14.0 ± 0.1 m")
print("9.0 ± 0.1 m")
print("16.0 ± 0.1 m")

print("\nFrequencies:")
print(f"{frequency[0]/1e6:.2f} ± {frequency_uncertainty[0]/1e6:.2f} MHz")
print(f"{frequency[1]/1e6:.2f} ± {frequency_uncertainty[1]/1e6:.2f} MHz")
print(f"{frequency[2]/1e6:.2f} ± {frequency_uncertainty[2]/1e6:.2f} MHz")
print(f"{frequency[3]/1e6:.2f} ± {frequency_uncertainty[3]/1e6:.2f} MHz")
print(f"{frequency[4]/1e6:.2f} ± {frequency_uncertainty[4]/1e6:.2f} MHz")
print(f"{frequency[5]/1e6:.2f} ± {frequency_uncertainty[5]/1e6:.2f} MHz")
print(f"{frequency[6]/1e6:.2f} ± {frequency_uncertainty[6]/1e6:.2f} MHz")
print(f"{frequency[7]/1e6:.2f} ± {frequency_uncertainty[7]/1e6:.2f} MHz")
print(f"{frequency[8]/1e6:.2f} ± {frequency_uncertainty[8]/1e6:.2f} MHz")
