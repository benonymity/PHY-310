import numpy as np
import matplotlib.pyplot as plt

file = open("data/Parallel 4.csv", "r")

# Skip header row
next(file)
next(file)

illumination = []
angle = []

for line in file:
    data = line.strip().split(',')
    if data[2] and data[1]:
        # if float(data[2]) < -2*np.pi:
            illumination.append(float(data[1]))
            angle_val = float(data[2])
            # Use modulo operator to handle 2pi rollover correctly 
            angle_val = angle_val % (2*np.pi)
            angle.append(angle_val)

# Convert to numpy arrays for easier manipulation
angle = np.array(angle)
illumination = np.array(illumination)

# Sort data by angle
sort_idx = np.argsort(angle)
angle = angle[sort_idx]
illumination = illumination[sort_idx]

plt.figure(figsize=(10,6))
plt.plot(angle, illumination, 'r.-', label='Raw data')
plt.xlabel('Angle (rad)')
plt.ylabel('Illumination (lux)')
plt.title('Illumination vs Angle')
plt.legend()
plt.grid(True)
plt.show()