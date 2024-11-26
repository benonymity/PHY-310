import numpy as np
import matplotlib.pyplot as plt
import glob
import os

def analyze_csv(filename):
    file = open(filename, "r")
    
    # Skip header rows
    next(file)
    next(file)
    
    illumination = []
    angle = []
    
    for line in file:
        data = line.strip().split(',')
        if data[2] and data[1]:
            illumination.append(float(data[1]))
            angle_val = float(data[2])
            angle_val = angle_val % (2*np.pi)
            angle.append(angle_val)
            
    file.close()
    
    # Convert to numpy arrays
    angle = np.array(angle)
    illumination = np.array(illumination)
    
    # Sort by angle
    sort_idx = np.argsort(angle)
    angle = angle[sort_idx]
    illumination = illumination[sort_idx]
    
    # Calculate RMS with error propagation
    # For sum of squares, relative error is doubled
    # For sqrt, relative error is halved
    # Overall relative error is same as original
    rms = np.sqrt(np.mean(illumination**2))
    rms_err = 0.1 * rms/np.mean(illumination)  # Relative error same as input
    
    # Find midpoint of angles
    mid_idx = len(angle)//2
    mid_angle = angle[mid_idx]
    
    # Get data around midpoint (±π/4 rad) to avoid edge effects
    mask = np.abs(angle - mid_angle) < np.pi/4
    filtered_illum = illumination[mask]
    
    # Find max/min excluding outliers
    max_val = np.percentile(filtered_illum, 95)  # 95th percentile instead of max
    min_val = np.percentile(filtered_illum, 5)   # 5th percentile instead of min
    
    # Error on max/min is same as measurement error
    max_err = 0.1
    min_err = 0.1
    
    return angle, illumination, rms, rms_err, max_val, max_err, min_val, min_err

# Get all CSV files
csv_files = glob.glob("data/*.csv")

for csv_file in csv_files:
    filename = os.path.basename(csv_file)
    angle, illumination, rms, rms_err, max_val, max_err, min_val, min_err = analyze_csv(csv_file)
    
    plt.figure(figsize=(12,8))
    # Plot with error bars
    plt.errorbar(angle, illumination, yerr=0.1, xerr=0.01, fmt='.-', label=f'{filename}')
    # Add horizontal lines for max and min
    plt.axhline(y=max_val, color='k', linestyle=':', alpha=0.5)
    plt.axhline(y=min_val, color='k', linestyle=':', alpha=0.5)
    
    plt.xlabel('Angle (rad)')
    plt.ylabel('Illumination (lux)')
    plt.title(f'Illumination vs Angle - {filename}')
    plt.legend()
    plt.grid(True)
    
    # Save figure
    plt.savefig(f'images/{filename[:-4]}.png')
    plt.close()
    
    print(f"\nResults for {filename}:")
    print(f"RMS: {rms:.2f} ± {rms_err:.2f} lux")
    print(f"Max: {max_val:.2f} ± {max_err:.2f} lux") 
    print(f"Min: {min_val:.2f} ± {min_err:.2f} lux")